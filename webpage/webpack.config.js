var webpack = require('webpack');
var path = require('path');
var UglifyJsPlugin = require('uglifyjs-webpack-plugin');

var BUILD_DIR = path.resolve(__dirname, 'src/client/public');
var APP_DIR = path.resolve(__dirname, 'src/client/app');

var config = {
  entry: APP_DIR + '/index.jsx',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        use: [{loader: 'babel-loader'}]
      }
    ]
  },
  optimization: {
    minimize: true,
    minimizer: [
      new UglifyJsPlugin({
        uglifyOptions: {
          warnings: false,
          parse: {},
          compress: {},
          mangle: true,
          output: null,
          toplevel: true,
          nameCache: null,
          ie8: false,
          keep_fnames: false,
        },
      }),
    ],
  },
  mode: 'production'
};

module.exports = config;