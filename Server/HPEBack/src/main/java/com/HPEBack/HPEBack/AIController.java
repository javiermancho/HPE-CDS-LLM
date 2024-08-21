package com.HPEBack.HPEBack;

import java.io.IOException;
import java.util.ArrayList;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@CrossOrigin(origins = "http://localhost:3000")
@RestController
public class AIController{

    @PostMapping("/llama")
    public static String getData(@RequestBody RequestData data) throws IOException, InterruptedException{
        String message = data.getMessage();
        String dateInit = data.getDateStart();
        String dateEnd = data.getDateEnd();

        String response = Requests.postEmbeddings(Utils.queryBuilder(message, Utils.convertDate(dateInit), Utils.convertDate(dateEnd)));
        
        System.out.println(response);

        ArrayList<String> chunks = Utils.extractTextFromEmbeddings(response);
        
        String responseFromModel = Requests.postllama(Utils.promptBuilder(message, chunks));

        return Utils.extractTextFromModel(responseFromModel);
    }

}




