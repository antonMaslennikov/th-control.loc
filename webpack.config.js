const path = require('path')

module.exports = {
    entry: './pages/static/js/index.js',
    output: {
        path: path.resolve(__dirname, './pages/static/'),
        filename: 'bundle.js'
    },
    mode: 'production'
}