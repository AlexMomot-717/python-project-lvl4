module.exports = {
  useTabs: false,
  plugins: [require("prettier-plugin-jinja-template")],
  overrides: [
    {
      files: ["*.html"],
      options: { parser: "jinja-template" },
      quoteAttributes: false
    },
  ]
}
