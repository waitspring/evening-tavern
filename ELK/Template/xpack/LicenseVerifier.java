/**********************************************************************************************************************
 *                          _                             _                   _                                       *
 *                       \_|_)  o                        (_|   |_/        o  | | o                                    *
 *                         |        __   _   _  _    ,   _ |   | _   ,_      | |     _   ,_                           *
 *                        _|    |  /    |/  / |/ |  / \_|/ |   ||/  /  |  |  |/  |  |/  /  |                          *
 *                       (/\___/|_/\___/|__/  |  |_/ \/ |__/\_/ |__/   |_/|_/|__/|_/|__/   |_/                        *
 *                                                                           |\                                       *
 *                                                                           |/                                       *
 **********************************************************************************************************************
 */

package org.elasticsearch.license;

import java.io.*;
import java.nio.*;
import java.security.*;
import java.util.*;

import org.apache.lucene.util.*;
import org.elasticsearch.common.bytes.*;
import org.elasticsearch.common.xcontent.*;
import org.elasticsearch.core.internal.io.*;

public class LicenseVerifier {

    public static boolean verifyLicense(final License license, byte[] publicKeyData) {
        return true;
    }

    public static boolean verifyLicense(final License license) {
        return true;
    }
}
