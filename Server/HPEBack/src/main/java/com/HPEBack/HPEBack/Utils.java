package com.HPEBack.HPEBack;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

public class Utils {
    public static String promptBuilder(String message){
        return "{ \"system_message\": \"Eres un asistente genial\", \"user_message\": \"" + message + "\", \"max_tokens\": 250 }";
    }

    public static String extractText(String response){
        Gson gson = new Gson();
        JsonObject jsonObject = gson.fromJson(response, JsonObject.class);
        JsonArray choicesArray = jsonObject.getAsJsonArray("choices");
        JsonObject choiceObject = choicesArray.get(0).getAsJsonObject();
        String text = choiceObject.get("text").getAsString();

        // Extraer el texto después de [/INST]
        String delimiter = "[/INST]";
        String extractedText = "";
        int index = text.indexOf(delimiter);
        if (index != -1) {
            extractedText = text.substring(index + delimiter.length()).trim();
        }

        return extractedText;
    }
}
