const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const DIST_FOLDER = 'public';

module.exports = {
    entry: './src/index.js',
    mode: 'development',
    output: {
        filename: '[name].[hash].bundle.js',
        publicPath: `/${DIST_FOLDER}`,
        path: path.resolve(__dirname, DIST_FOLDER)
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "sass-loader"
                }]
            },
            {
                test: /\.vue$/,
                use: [{
                    loader: "vue-loader"
                }]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin([DIST_FOLDER]),
        new HtmlWebpackPlugin({
            title: 'Atlas',
            template: './src/index.html'
        })
    ],
};