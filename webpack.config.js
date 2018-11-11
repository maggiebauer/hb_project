const path = require('path');

module.exports = {
  entry: './static/js/search.jsx',
  output: {
    filename: 'main.js',
    path: path.join(__dirname, 'dist')
  },
  module:  {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options:  {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react'
            ],
            plugins: [
              '@babel/plugin-proposal-object-rest-spread',
              "transform-class-properties",
              "@babel/plugin-proposal-export-default-from",
              "transform-react-jsx"
            ]
          },

        }
      }
    ]
  }
};