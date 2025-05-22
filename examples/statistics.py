from py_spoo_url import Statistics

statistics = Statistics("ga")
# in case of password protected urls, pass the password after the shortcode
# for Emoji Urls pass the emoji sequence

print(statistics.long_url)
print(statistics.average_daily_clicks)
print(statistics.average_monthly_clicks)
print(statistics.average_weekly_clicks)
print(statistics.total_clicks)
print(statistics.total_unique_clicks)
print(statistics.max_clicks)
print(statistics.last_click)
print(statistics.last_click_browser)
print(statistics.last_click_platform)
print(statistics.created_at)
print(statistics.creation_time)
print(statistics.browsers_analysis)
print(statistics.platforms_analysis)
print(statistics.country_analysis)
print(statistics.referrers_analysis)
print(statistics.clicks_analysis)
print(statistics.unique_browsers_analysis)
print(statistics.unique_platforms_analysis)
print(statistics.unique_country_analysis)
print(statistics.unique_referrers_analysis)
print(statistics.unique_clicks_analysis)
print(statistics.expired)

print(statistics.last_n_days_analysis(7))

plt = statistics.make_chart(statistics.browsers_analysis)
plt.show()

plt = statistics.make_chart(statistics.last_n_days_analysis, "bar", days=6)
plt.show()

plt = statistics.make_countries_heatmap()
plt.show()
