// module.exports = {
//   publicPath: process.env.BASE_PATH || "/", // <-- this is correct now (and default)
//   transpileDependencies: ["vuetify"],
// };

// const path = require('path')

// module.exports = {
//     devServer: {
//         proxy: {
//             '/api/': {
//                 target: 'https://auctionportalbackend.herokuapp.com/',
//                 changeOrigin: true,
//                 secure: false,
//                 pathRewrite: { '^/api': 'https://auctionportalbackend.herokuapp.com' + '/api' },
//                 logLevel: 'debug'
//             },
//         }
//     }
// }

module.exports = {

    configureWebpack: {
        devServer: {
            historyApiFallback: true
        }
    },


};