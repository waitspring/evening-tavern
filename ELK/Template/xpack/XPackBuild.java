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
    private String shortHash;
    private String date;

    @SuppressForbidden(reason = "looks up path of xpack.jar directly")
    static Path getElastic
}
