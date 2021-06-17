//
//  calculate.js - functions supporting various caclulations
//


function calculateMedianGPA(gpas){
    return gpas.length ? (Math.round(math.median(gpas) * 100) / 100).toFixed(2) : 0;
}

function calculateCourseMedian(grades) {
    return (grades.length) ? (Math.round(math.median(grades) * 100) / 100).toFixed(2) : 'None';
}

function calculateFailedPercentage(course_grades) {
    var failed = 0;

    for (var g = 0; g < course_grades.length; g++) {
        if (course_grades[g] <= 0.7) {
            failed += 1;
        }
    }

    return (course_grades.length > 0) ? Math.round((failed * 100)/ course_grades.length) : 0;
}
