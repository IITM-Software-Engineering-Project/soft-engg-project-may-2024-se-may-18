export default {
    setEnrolledCourses(state: { enrolledCourses: any; }, courses: any) {
        state.enrolledCourses = courses;
    },
    setAllCourses(state: { allCourses: any; }, courses: any) {
        state.allCourses = courses;
    },
    addEnrolledCourse(state: { allCourses: any[]; enrolledCourses: any[]; }, courseId: any) {
        const course = state.allCourses.find((course: { id: any; }) => course.id === courseId);
        if (course) {
            state.enrolledCourses.push(course);
        }
    },
    setLoadingFetchingEnrolledCourses(state: { loading: { fetchingEnrolledCourses: string; }; }, loading: string) {
        state.loading.fetchingEnrolledCourses = loading;
    },
    setLoadingFetchingAllCourses(state: { loading: { fetchingAllCourses: string; }; }, loading: string) {
        state.loading.fetchingAllCourses = loading;
    },
};