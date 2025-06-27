module.exports = {
  devServer: {
    proxy: {
      '^/auth': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '^/posts': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '^/profile': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '^/admin': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    },
  },
};
