package com.HPEBack.HPEBack;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class RequestData {
    
    private String message;
    
    private String dateStart;
    
    private String dateEnd;

    // Getters y Setters
    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getDateStart() {
        return dateStart;
    }

    public void setDateStart(String dateStart) {
        this.dateStart = dateStart;
    }

    public String getDateEnd() {
        return dateEnd;
    }

    public void setDateEnd(String dateEnd) {
        this.dateEnd = dateEnd;
    }


    public static boolean dateVerifier(String date1, String date2){
         DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        // Convertir las cadenas a objetos LocalDate
        LocalDate localDate1 = LocalDate.parse(date1, formatter);
        LocalDate localDate2 = LocalDate.parse(date2, formatter);
        
        return localDate1.isAfter(localDate2);
    }
}

