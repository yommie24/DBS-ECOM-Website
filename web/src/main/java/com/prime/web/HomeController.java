package com.prime.web;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {
    Logger log = LoggerFactory.getLogger(HomeController.class);

    @GetMapping("/hi")
    public String hi() {
        return "Hi, this works without auth";
    }

    @GetMapping("/his")
    public String his() {
        log.info("/his was visited.");
        return "Hi, this requires auth";
    }
}
