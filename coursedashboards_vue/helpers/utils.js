export const toSectionLabel = (params) => {
  return (
    params.year +
    "-" +
    params.quarter +
    "-" +
    params.curriculum +
    "-" +
    params.course_number +
    "-" +
    params.section_id
  );
};
