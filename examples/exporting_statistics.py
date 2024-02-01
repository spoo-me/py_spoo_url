from py_spoo_url import Statistics

statistics = Statistics("ga")

# xslx
statistics.export_data("export.xlsx", "xlsx")

# csv
statistics.export_data("export", "csv")  # this will return a zip file

# json
statistics.export_data("export.json", "json")
