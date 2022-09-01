import { createStore } from "vuex";

const store = createStore({
  state: {
    name: "Vue",
    csrfToken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
  },
});

export default store;
