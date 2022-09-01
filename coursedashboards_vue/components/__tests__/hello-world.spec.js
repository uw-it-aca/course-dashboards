import { mount } from "@vue/test-utils";
import HelloWorld from "../hello-world.vue";

test("displays hello world", () => {
  const wrapper = mount(HelloWorld);
  // Assert the rendered text of the component
  expect(wrapper.text()).toContain("Hello world");
});
