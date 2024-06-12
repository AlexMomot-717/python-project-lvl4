const config = {
  plugins: [require.resolve("prettier-plugin-jinja-template")],
  useTabs: true,
  overrides: [{
    "files": ["*.html"],
    "options": {
      "parser": "jinja-template"
    }
  }]
};

module.exports = config;
