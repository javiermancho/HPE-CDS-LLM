package com.HPEBack.HPEBack;

import java.io.IOException;
import java.util.ArrayList;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@CrossOrigin(origins = "http://localhost:3000")
@RestController
public class AIController{

    @PostMapping("/llama")
    public static ResponseEntity<String> getData(@RequestBody RequestData data) throws IOException, InterruptedException{
        String message = data.getMessage();
        String dateInit = data.getDateStart();
        String dateEnd = data.getDateEnd();

        if (dateInit.equals("") || dateEnd.equals("") || message.equals("")){
            return ResponseEntity.badRequest().body("Por favor, introduce todos los campos");
        }
        else if (RequestData.dateVerifier(dateInit, dateEnd)){
            return ResponseEntity.badRequest().body("La fecha de inicio no puede ser posterior a la fecha de fin");
        }
        try{
            
            String response = Requests.postEmbeddings(Utils.queryBuilder(message, Utils.convertDate(dateInit), Utils.convertDate(dateEnd)));
            
            System.out.println(response);
            ArrayList<String> chunks = Utils.extractTextFromEmbeddings(response);

            String responseFromModel = Requests.postllama(Utils.promptBuilder(message, chunks));
            String text = Utils.extractTextFromModel(responseFromModel); 
            
            String finalResponse = Utils.completeResponse(text, response);
            return ResponseEntity.ok().body(finalResponse);
        }
        catch(Exception e){
            return ResponseEntity.badRequest().body("No files found");
        }
    }
        
}




