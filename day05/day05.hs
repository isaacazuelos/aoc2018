#! /usr/bin/env stack
-- stack --resolver lts-12.21 script

module Main where

main = do
    polymer <- readFile "input.txt"
    print $ length polymer

