package com.HPEBack.HPEBack;

import java.lang.reflect.Array;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

public class Utils {
    public static String promptBuilder(String message, ArrayList<String> chunks){
        // Crear un prompt con los chunks
        String prompt = "¿Puedes responderme a la siguiente pregunta: " + message + "utilizando los siguientes párrafos como contexto? ";
        for (String chunk : chunks) {
            prompt += chunk + ".";
        }

        return "{ \"system_message\": \"Eres un asistente legal encargado de sintetizar el contenido del boletin oficial del estado de España. Asegurate que tus respuestas son concisas y claras.\", \"user_message\": \"" + prompt + "\", \"max_tokens\": 1024 }";
    }
    public static String queryBuilder(String text, String dateInit, String dateEnd){
        return "{ \"query\": \"" + text + "\", \"dateInit\": \"" + dateInit + "\", \"dateEnd\": \"" + dateEnd + "\" }";
    }

    public static String extractTextFromModel(String response){
        Gson gson = new Gson();
        JsonObject jsonObject = gson.fromJson(response, JsonObject.class);
        JsonArray choicesArray = jsonObject.getAsJsonArray("choices");
        JsonObject choiceObject = choicesArray.get(0).getAsJsonObject();
        String text = choiceObject.get("text").getAsString();

        // // Extraer el texto después de [/INST]
        // String delimiter = "[/INST]";
        // String extractedText = "";
        // int index = text.indexOf(delimiter);
        // if (index != -1) {
        //     extractedText = text.substring(index + delimiter.length()).trim();
        // }
        // System.out.println("Extracted text: " + extractedText);

        System.out.println(text);

        return text;
    }

    public static ArrayList<String> extractTextFromEmbeddings(String json){
        Gson gson = new Gson();

        // Convertir JSON a un objeto JsonObject
        JsonObject jsonObject = gson.fromJson(json, JsonObject.class);

        // Extraer el contenido de "content"
        JsonArray contentArray = jsonObject.getAsJsonArray("content").get(0).getAsJsonArray();

        // Convertir a una lista de String
        ArrayList<String> contentList = new ArrayList<>();
        for (int i = 0; i < contentArray.size(); i++) {
            System.out.println(contentArray.get(i).getAsString());
            String content = contentArray.get(i).getAsString().replace("\n", ". ");
            contentList.add(content);
        }

        return contentList;
    }

    public static String convertDate(String inputDate) {
        // Definir el formato de entrada
        System.out.println(inputDate);
        DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        // Parsear la fecha de entrada
        LocalDate date = LocalDate.parse(inputDate, inputFormatter);
        
        // Definir el formato de salida
        DateTimeFormatter outputFormatter = DateTimeFormatter.ofPattern("yyyyMMdd");
        
        // Formatear la fecha a la salida deseada
        return date.format(outputFormatter);
    }
}
