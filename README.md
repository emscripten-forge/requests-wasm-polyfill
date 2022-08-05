# requests-wasm-polyfill

A kind of drop in replacement for some parts of the requests library for wasm python.

Note that these only work when running under a web-worker, as it's making blocking HTTP requests which are not allowed in the main thread.
