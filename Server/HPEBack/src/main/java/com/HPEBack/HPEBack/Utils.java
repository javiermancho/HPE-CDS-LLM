package com.HPEBack.HPEBack;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Array;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


public class Utils {

    public static String createLink(String date, String id){
        String year = date.substring(0, 4);
        String month = date.substring(4, 6);
        String day = date.substring(6, 8);

        String[] links = id.split("-");

        return "https://www.boe.es/boe/dias/" + year + "/" + month + "/" + day + "/pdfs/" + links[0] + "-" + links[1] + "-" + links[2] + "-" + links[3] + ".pdf";
    }

    public static String purgarTexto(String input) {
        return input.replaceAll("[^a-zA-Z0-9\\s.,;:¿?¡!\n]", "");
    }

    public static String promptBuilder(String message, ArrayList<String> chunks){
        // Crear un prompt con los chunks
        String prompt = "¿Puedes responderme a la siguiente pregunta: " + message + "utilizando los siguientes párrafos como contexto? ";
        
        for (String chunk : chunks) {
            prompt += purgarTexto(chunk) + ". ";
        }

        
        return "{ \"system_message\": \"Eres un asistente legal encargado de sintetizar el contenido del boletin oficial del estado de España. Asegurate que tus respuestas son concisas y claras. No respondas con datos que no estén en el contexto que recibas del usuario.\", \"user_message\": \"" + prompt + "\", \"max_tokens\": 4096 }";
    }
    public static String queryBuilder(String text, String dateInit, String dateEnd){
        return "{ \"query\": \"" + text + "\", \"dateInit\": \"" + dateInit + "\", \"dateEnd\": \"" + dateEnd + "\" }";
    }

    public static String extractTextFromModel(String response){
        Gson gson = new Gson();
        System.out.println(response);
        // Parse the JSON string into a JsonObject
        JsonObject jsonObject = gson.fromJson(response, JsonObject.class);
        JsonElement responseElement = jsonObject.get("response");
        return responseElement.getAsString();
    }

    public static ArrayList<String> extractTextFromEmbeddings(String json){
        Gson gson = new Gson();

        JsonObject jsonObject = gson.fromJson(json, JsonObject.class);

        JsonArray contentArray = jsonObject.getAsJsonArray("content").get(0).getAsJsonArray();
        ArrayList<String> contentList = new ArrayList<>();
        for (int i = 0; i < contentArray.size(); i++) {
            String content = contentArray.get(i).getAsString().replace("\n", ". ");
            contentList.add(content);
        }

        return contentList;
    }

    public static String convertDate(String inputDate) {
        // Definir el formato de entrada
        DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        // Parsear la fecha de entrada
        LocalDate date = LocalDate.parse(inputDate, inputFormatter);
        
        // Definir el formato de salida
        DateTimeFormatter outputFormatter = DateTimeFormatter.ofPattern("yyyyMMdd");
        
        // Formatear la fecha a la salida deseada
        return date.format(outputFormatter);
    }

    public static String completeResponse(String responseLLM, String responseEmbeddings){
        // Completar la respuesta con los ids
        
        JsonObject jsonObject = JsonParser.parseString(responseEmbeddings).getAsJsonObject();
        // Extract dates
        JsonArray datesArray = jsonObject.getAsJsonArray("date");
        JsonArray firstDateArray = datesArray.get(0).getAsJsonArray();
        ArrayList<Integer> dates = new ArrayList<>();
        for (JsonElement dateElement : firstDateArray) {
            JsonObject dateObject = dateElement.getAsJsonObject();
            dates.add(dateObject.get("date").getAsInt());
        }

        // Extract IDs
        JsonArray idsArray = jsonObject.getAsJsonArray("ids");
        JsonArray firstIdsArray = idsArray.get(0).getAsJsonArray();

        ArrayList<String> ids = new ArrayList<>();
        for (JsonElement idElement : firstIdsArray) {
            String id = idElement.getAsString();
            ids.add(id);
        }

        String response = responseLLM + " Puedes encontrar más información en los siguientes enlaces: ";
        // Create links
        for (int i = 0; i < dates.size(); i++) {
            String link = createLink(dates.get(i).toString(), ids.get(i));
            response += (i+1) + ") " + link + " ";
        }

        // Add links to the response

        return response;
    }

}
