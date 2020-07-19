const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');

const BUILD_DIR = path.resolve(__dirname, 'src/client/public');
const APP_DIR = path.resolve(__dirname, 'src/client/app');

const config = {
    entry: APP_DIR + '/index.jsx',
    output: {
        path: BUILD_DIR,
        filename: 'index_bundle.js'
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
    plugins: [
        new HtmlWebpackPlugin({
            inject: true,
            minify: true,
            inlineSource: '.(js|css)$',
            filename: 'index.html',
            template: 'src/client/index.html'
        }),
        new HtmlWebpackInlineSourcePlugin()
    ],
    mode: 'production'
};

module.exports = config;