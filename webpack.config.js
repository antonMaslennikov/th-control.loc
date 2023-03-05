const path = require('path')

module.exports = {
    entry: './pages/static/js/index.js',
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
    output: {
        path: path.resolve(__dirname, './pages/static/'),
        filename: 'bundle.js'
    },
    mode: 'production'
}