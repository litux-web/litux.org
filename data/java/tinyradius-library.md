type: article
title: TinyRadius Java Library
last-updated: 2014-02-17
meta-keywords: TinyRadius, Java, GitHub, Fork

> TinyRadius is a simple, small and fast Java Radius library capable of sending and receiving Radius packets of all types. It is released under the terms of the LGPL.

`RADIUS` is a networking protocol used for authenticating, authorizing, and accounting for users on a network. It is commonly used in conjunction with 802.1x, a port-based network access control protocol, to provide secure access to networks.

The `TinyRadius` library can be used to develop `RADIUS` clients and servers. It supports both the `UDP` and `TCP` transport protocols, and it can be used to send and receive `RADIUS` packets of all types. The library is also thread-safe, making it suitable for use in multi-threaded applications.

The `TinyRadius` library is a valuable tool for developing `RADIUS` clients and servers. It is simple to use, efficient, and thread-safe. The library is also open source, making it a great choice for developers who want to customize the library to meet their specific needs.

I forked the library to add performance optimizations for high-volume multi-threaded applications and added or fixed many vendor-specific `RADIUS` attributes.

My fork of `TiyRadius` is available at [github.com/davipt/TinyRadius](https://github.com/davipt/TinyRadius), and all changes can be seen [on this combined diff](https://github.com/davipt/TinyRadius/compare/rel-1.0.0...master).

The original site for `TinyRadius` is available at [tinyradius.sourceforge.net](https://tinyradius.sourceforge.net), and it was developed by Matthias Wuttke.

