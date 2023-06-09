type: article
title: GeoIP API Java Library
last-updated: 2014-12-15
meta-keywords: MaxMind, GeoIP, Java, GitHub, Fork

My fork of MaxMind's `geoip-api` v1 (legacy format) is at [github.com/davipt/geoip-api-java](https://github.com/davipt/geoip-api-java).

Albeit the v1 dataset is considered legacy and the new v2 `mmdb` should be used, some information is lacking or not as easily accesible on the new dataset, so we stuck to the legacy database and library.

This fork contains performance optimizations for high volume multi-threaded applications, namely by removing the `synchronized` on calls where the data is only being read and only locking the code if the database is reloaded on-the-fly.

