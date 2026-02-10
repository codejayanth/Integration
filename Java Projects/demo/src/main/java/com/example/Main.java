package com.example;

import org.apache.flink.table.api.*;

import static org.apache.flink.table.api.Expressions.*;

public class Main {
    public static void main(String[] args) {

        TableEnvironment tableEnv = TableEnvironment.create(
                EnvironmentSettings.newInstance().inStreamingMode().build()
        );

        // Source: Generates random data
        tableEnv.executeSql(
                "CREATE TABLE Orders (" +
                "  `user` BIGINT, " +
                "  product STRING, " +
                "  amount INT" +
                ") WITH (" +
                "  'connector' = 'datagen'," +
                "  'rows-per-second' = '5'" +
                ")"
        );

        // Sink: Discards results but allows job execution
        tableEnv.executeSql(
                "CREATE TABLE Result (" +
                "  `user` BIGINT," +
                "  cnt BIGINT" +
                ") WITH (" +
                "  'connector' = 'blackhole'" +
                ")"
        );

        Table orders = tableEnv.from("Orders");

        Table counts = orders
                .groupBy($("user"))
                .select($("user"), $("product").count().as("cnt"));

        counts.executeInsert("Result");
    }
}
