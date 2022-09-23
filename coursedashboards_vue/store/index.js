import { createStore } from "vuex";

const store = createStore({
  state: {
    name: "Vue",
    csrfToken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
    year: JSON.parse(document.getElementById("year").textContent),
    quarter: JSON.parse(document.getElementById("quarter").textContent),
  },
});

export default store;
