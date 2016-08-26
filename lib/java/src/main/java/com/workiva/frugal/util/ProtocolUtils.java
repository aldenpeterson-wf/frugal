package com.workiva.frugal.util;

import java.nio.charset.Charset;

/**
 * Utilities for reading/writing protocol data.
 */
public class ProtocolUtils {

    public static int readInt(byte[] buff, int offset) {
        return ((buff[offset] & 0xff) << 24) |
                ((buff[offset + 1] & 0xff) << 16) |
                ((buff[offset + 2] & 0xff) << 8) |
                (buff[offset + 3] & 0xff);
    }

    public static void writeInt(int i, byte[] buff, int offset) {
        buff[offset] = (byte) (0xff & (i >> 24));
        buff[offset + 1] = (byte) (0xff & (i >> 16));
        buff[offset + 2] = (byte) (0xff & (i >> 8));
        buff[offset + 3] = (byte) (0xff & (i));
    }

    public static void writeString(String s, byte[] buff, int offset) {
        byte[] strBytes = Charset.forName("UTF-8").encode(s).array();
        System.arraycopy(strBytes, 0, buff, offset, s.length());
    }

    /**
     * Encodes a string using UTF-8.
     *
     * @param s The string to encode.
     * @return The bytes representing the string.
     */
    public static byte[] encodeString(String s) {
        return s.getBytes(Charset.forName("UTF-8"));
    }

    /**
     * Writes the bytes corresponding to a UTF-8 encoded string into a buffer,
     * starting at a certain offset.
     *
     * @param strBytes The bytes to write.
     * @param buff The buffer to write into.
     * @param offset The position in buff to start writing at.
     */
    public static void writeStringBytes(byte[] strBytes, byte[] buff, int offset) {
        System.arraycopy(strBytes, 0, buff, offset, strBytes.length);
    }

}
