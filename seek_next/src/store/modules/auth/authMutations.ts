export default {
    setUser(state: { user: any; }, user: any) {
        state.user = user;
        localStorage.setItem("user", JSON.stringify(user));
    },
    setAccessToken(state: { accessToken: any; }, accessToken: string) {
        state.accessToken = accessToken;
        localStorage.setItem("accessToken", accessToken);
    },
    setLoggedIn(state: { isLoggedIn: any; }, isLoggedIn: any) {
        state.isLoggedIn = isLoggedIn;
        localStorage.setItem("isLoggedIn", JSON.stringify(isLoggedIn));
    },
    clearAuthData(state: { user: { id: string; name: string; email: string; role: string; }; accessToken: null; isLoggedIn: boolean; }) {
        state.user = { id: "", name: "", email: "", role: "" };
        state.accessToken = null;
        state.isLoggedIn = false;
        localStorage.removeItem("user");
        localStorage.removeItem("accessToken");
        localStorage.removeItem("isLoggedIn");
    },
    setRedirectPath(state: { redirectPath: any; }, path: string) {
        state.redirectPath = path;
    },
    setCurrentMessage(state: { currentMessage: any; }, message: string) {
        state.currentMessage = message;
    }
};