export default {
    setCreatedCourses(state: { createdCourses: any[] }, courses: any[]) {
        state.createdCourses = courses;
    },
    setLoadingFetchingCreatedCourses(state: { loading: { fetchingCreatedCourses: string } }, loading: string) {
        state.loading.fetchingCreatedCourses = loading;
    },
};
