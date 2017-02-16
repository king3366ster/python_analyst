// const env = require('./env')
const path = require('path')
const postcss = require('postcss')
const precss = require('precss')

let config = {
  input: './webapp/src/css/**/*.css',
  dir: './webapp/dist/css',
  'local-plugins': true,
  use: [
    'precss',
    // 'postcss-import',
    'postcss',
    'postcss-custom-properties',
    'postcss-calc',
    'postcss-simple-vars',
    'postcss-mixins',
    'postcss-nested',
    // 'postcss-scss',
    // 'cssnano',
    // 'autoprefixer',
    'postcss-cssnext'
  ],
  autoprefixer: {
    browsers: ['Android >= 4', 'iOS >= 7', 'Chrome >= 10', 'Firefox >= 10', 'IE >= 8']
  }
}

// if (env.isProduction()) {
//   config.use.push('cssnano')
//   config.map = false
// } else {
//   config.map = 'inline'
// }

module.exports = config
