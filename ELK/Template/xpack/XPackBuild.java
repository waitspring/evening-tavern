/**********************************************************************************************************************
 *                                _      , __             _   , __            _                                       *
 *                               (_\  / /|/  \           | | /|/  \       o  | |    |                                 *
 *                                  \/   |___/ __,   __  | |  | __/          | |  __|                                 *
 *                                  /\   |    /  |  /    |/_) |   \|   |  |  |/  /  |                                 *
 *                                _/  \_/|    \_/|_/\___/| \_/|(__/ \_/|_/|_/|__/\_/|_/                               *
 *                                                                                                                    *
 *                                                                                                                    *
 **********************************************************************************************************************
 */

package org.elasticsearch.xpack.core;

import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.jar.*;

import org.elasticsearch.common.*;

public class XPackBuild {

    public static final XPackBuild CURRENT;

    static {
        final String shortHash;
        final String date;

        Path path = getElasticsearchCodebase();
        if (path.toString().endsWith(".jar")) {
            try (JarInputStream jar = new JarInputStream(Files.newInputStream(path))) {
                Manifest manifest = jar.getManifest();
                shortHash = "Unknown";
                date = "Unknown";
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        } else {
            shortHash = "Unknown";
            date = "Unknown";
        }

        CURRENT = new XPackBuild(shortHash, date);
    }

    @SuppressForbidden(reason = "looks up path of xpack.jar directly")
    static Path getElasticsearchCodebase() {
        URL url = XPackBuild.class.getProtectionDomain().getCodeSource().getLocation();
        try {
            return PathUtils.get(url.toURI());
        } catch (URISyntaxException bogus) {
            throw new RuntimeException(bogus);
        }
    }

    private String shortHash;
    private String date;

    XPackBuild(String shortHash, String date) {
        this.shortHash = shortHash;
        this.date = date;
    }

    public String shortHash() {
        return shortHash;
    }

    public String date() {
        return date;
    }
}
