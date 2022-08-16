// import "regenerator-runtime/runtime";
import axios from "axios";

const courseDataMixin = {
  methods: {
    $_getAxiosConfig: function () {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
          "X-CSRFToken": csrfToken,
        },
      };
      return axiosConfig;
    },
    getIntroModalStatus: async function (uwnetid) {
      return axios.get(
        "/api/v1/user/" + uwnetid + "/introduction",
        {},
        this.$_getAxiosConfig()
      );
    },
    setIntroModalSeen: async function (uwnetid) {
      return axios.post(
        "/api/v1/user/" + uwnetid + "/introduction",
        {
          seen: true,
          introductionVersion: 1,
        },
        this.$_getAxiosConfig()
      );
    },
    // saveStudent: async function (systemkey, programs) {
    //   return axios.post(
    //     "/api/internal/student/save/",
    //     {
    //       system_key: systemkey,
    //       programs: programs,
    //     },
    //     this.$_getAxiosConfig()
    //   );
    // },
    // getPrograms: async function () {
    //   return axios.get("/api/internal/programs/", {}, this.$_getAxiosConfig());
    // },
  },
};

export default courseDataMixin;
