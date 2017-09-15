import statistics
from django.db import models
from coursedashboards.dao.section import get_past_offering_of_course
from coursedashboards.models import Course, Term
from coursedashboards.models.major import StudentMajor, CourseMajor
from coursedashboards.models.registration import Registration


class CourseOffering(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)
    current_enrollment = models.PositiveSmallIntegerField()
    limit_estimate_enrollment = models.PositiveSmallIntegerField()
    canvas_course_url = models.CharField(max_length=2000)
    # num_repeating = models.IntegerField()
    # median_gpa = models.FloatField()

    def calculate(self):
        """
        Calculates the course offering metadata for display in the UI
        """
        self.num_repeating = 0

        registrations = self.get_registrations()

        grades = []
        majors = {}
        concurrent_registrations = []

        for reg in registrations:
            if reg.is_repeat:
                self.num_repeating += 1

            student = reg.user

            # load the grade
            if reg.grade is not "X":
                grades.append(float(reg.grade))

            # load the major
            student_majors = StudentMajor.objects.filter(user=student)

            for student_major in student_majors:
                if student_major in majors:
                    majors[student_major] += 1
                else:
                    majors[student_major] = 1

            # retrieve any concurrent registrations for concurrent courses
            concurrent_regs = Registration.objects.filter(user=student,
                                                          term=reg.term)
            concurrent_registrations += concurrent_regs

        # calculate the median GPA
        self._calculate_grade_distribution(grades)

        self.course_majors = []
        # Save the # of each major
        for major in majors:
            course_major = CourseMajor(major=major, count=majors[major],
                                       course=self.course)
            # TODO : ask Mike if we should save this or add to self
            self.course_majors.append(course_major)

    def _calculate_grade_distribution(self, grades):
        """
        Performs the processing to generate the distribution data about
        GPA for a given section
        :param grades: a list of grades. floats
        """
        if not len(grades):
            return

        self.median_gpa = statistics.median(grades)

    def _calculate_concurrent_courses(self, concurrent_registrations):
        """
        Takes in a dict of the concurrent courses being taken and
        :param concurrent_registrations: a dict of Course : num_taking (int)
        """

        concurrent_courses = {}
        self.concurrent_courses = []

        for reg in concurrent_registrations:

            if reg.course in concurrent_courses:
                concurrent_courses[reg.course] += 1
            else:
                concurrent_courses[reg.course] = 1

        for course in concurrent_courses:
            # Check if we've loaded this already in the DB on the other course
            if ConcurrentCourse.objects.exists(course_info=self.course,
                                               course=course):
                model = ConcurrentCourse.objects.get(course_info=self.course,
                                                     course=course)
                self.concurrent_courses.append(model)
                continue

            concurrent = ConcurrentCourse()
            concurrent.course_offering = self
            concurrent.concurrent_course = course
            concurrent.count = concurrent_courses[course]

            # concurrent.save()

            self.concurrent_courses.append(concurrent)

            # save the opposite

            concurrent = ConcurrentCourse()
            concurrent.course_offering = CourseOffering.objects.get(course=course)
            concurrent.concurrent_course = self.course
            concurrent.count = concurrent_courses[course]
            # concurrent.save()

    def get_registrations(self):
        """
        Returns a QuerySet of Registration objects matching this course.
        :return: QuerySet object
        """
        return Registration.objects.filter(term=self.term,
                                           course=self.course)

    def json_object(self):
        offering_json = {}
        offering_json['curriculum'] = self.course.curriculum
        offering_json['course_number'] = self.course.course_number
        offering_json['section_id'] = self.course.section_id
        offering_json['current_enrollment'] = self.current_enrollment
        offering_json['limit_estimate_enrollment'] = (
            self.limit_estimate_enrollment)
        offering_json['current_median'] = self.median

        concurrent_courses = []

        for course in self.concurrent_courses:
            concurrent_courses.append(course.json_object())

        offering_json['concurrent_courses'] = concurrent_courses
        offering_json['current_student_majors'] = self.course_majors

        offering_json['past_offerings'] = get_past_offering_of_course(
            self.course.curriculum,
            self.course.course_number, self.term)

        return offering_json

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')

    @classmethod
    def load(cls, course, term):
        """
        Retrieves a CourseOffering object from data in the SWS
        :param course:
        :param term:
        :return:
        """
        raise CourseOffering.DoesNotExist


class ConcurrentCourse(models.Model):
    course_offering = models.ForeignKey(CourseOffering,
                                        on_delete=models.PROTECT)
    concurrent_course = models.ForeignKey(Course,
                                          on_delete=models.PROTECT)
    count = models.IntegerField()

    def json_object(self):

        course_str = str(self.concurrent_course)

        percentage = round(float(self.count) /
                           float(self.course_offering.current_enrollment) * 100
                           , 2)

        concurrent_json = {
            "course":  course_str,
            "number_students": self.course_offering.current_enrollment,
            "percent_students": percentage
            }

        return concurrent_json

