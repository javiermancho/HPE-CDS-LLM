package com.HPEBack.HPEBack;

import java.io.IOException;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;


@CrossOrigin(origins = "http://localhost:3000")
@RestController
public class AIController{

    @PostMapping("/llama")
    public static String getData(@RequestBody String message) throws IOException, InterruptedException{
        System.out.println(message);

        String response = Requests.postllama(Utils.promptBuilder(message));
        return Utils.extractText(response);
    }

}




