package com.example.restapi.controller;

import com.example.restapi.model.Row;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/rows")
public class RowsController {
    private final List<Row> rows = new ArrayList<>();

    @GetMapping
    public List<Row> getAllRows() {
        return rows;
    }

    @GetMapping("/{id}")
    public Row getRowById(@PathVariable int id) {
        return rows.stream().filter(r -> r.getId() == id).findFirst().orElse(null);
    }

    @PostMapping
    public Row addRow(@RequestBody Row row) {
        rows.add(row);
        return row;
    }

    @DeleteMapping("/{id}")
    public void deleteRow(@PathVariable int id) {
        rows.removeIf(r -> r.getId() == id);
    }
}