package com.HPEBack.HPEBack;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Requests {
    //Http request POST to 127:0.0.1:5000/llama
    public static String postllama(String body) throws IOException, InterruptedException{

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://llm:5003/llama"))
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .header("content-type", "application/json")
                .build();
        String response = client.send(request, HttpResponse.BodyHandlers.ofString()).body();
        
        return response;
    }

    //Http request POST to 127:0.0.1:5000/embeddings
    public static String postEmbeddings(String body) throws IOException, InterruptedException{

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://chromadb:5000/query"))
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .header("content-type", "application/json")
                .build();
        String response = client.send(request, HttpResponse.BodyHandlers.ofString()).body();


        return response;
    }


    // Cliente manda el mensaje al servidor {text}
    // Servidor manda el mensaje a la bbdd /query y devuelve los chunks
    /*
     * {
     *  "text": "Pregunta"
     *  "Contexto": "Contexto"
     * }
     */
    // Servidor manda el mensaje mas los chunks al modelo

}

