#!/usr/bin/env ruby

def main


  rand_url = "https://www.douban.com/group/topic/129019947/"

  sleep_seconds = rand(1000)
  puts "Sleep #{sleep_seconds} for a while."
  sleep(sleep_seconds)

  case RUBY_PLATFORM
  when /darwin/
    `open -g #{rand_url}`
  when /linux/
    `xdg-open #{rand_url}`
  end
end

if __FILE__ == $0
  main
end
