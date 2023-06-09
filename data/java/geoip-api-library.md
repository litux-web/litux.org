type: article
title: GeoIP API Java Library
last-updated: 2014-12-15
meta-keywords: MaxMind, GeoIP, Java, GitHub, Fork


The GeoIP API Java Library is a comprehensive library that provides a simple and efficient way to determine the geographic location of IP addresses. The library uses the MaxMind GeoIP v1 Format. The library supports both IPv4 and IPv6 addresses, and it can be used to determine the country, region, city, and postal code of an IP address.

The GeoIP API Java Library is easy to use. The library provides a simple API that can be used to perform geographic lookups. The library also provides a number of features that make it easy to integrate with other applications, such as support for caching and multithreading.

There are a number of benefits to using the GeoIP API Java Library. The library is accurate, reliable, and easy to use. The library is also free and open source, which makes it a great choice for developers who are looking for a cost-effective and reliable solution for determining the geographic location of IP addresses.


I forked the library to add performance optimizations for high-volume multi-threaded applications. Namely by removing the unnecessary `synchronized` on calls where the data is only being read and only locking the code if the database is reloaded on-the-fly.

My fork of MaxMind's `geoip-api` v1 (legacy format) is available at [github.com/davipt/geoip-api-java](https://github.com/davipt/geoip-api-java).

Although the v1 dataset is considered legacy and the new v2 `mmdb` should be used, some information is available on v1 and still missing on v2, or not as easily accessible on the new dataset, so we stuck to the legacy database and library.

