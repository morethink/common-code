#!/usr/bin/env bash
set -e
cd /Users/liwenhao/Desktop/github/blog
hexo clean
hexo generate
hexo douban
hexo serve
