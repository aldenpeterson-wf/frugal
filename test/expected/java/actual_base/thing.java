/**
 * Autogenerated by Frugal Compiler (1.18.0)
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *
 * @generated
 */
package actual_base.java;

import org.apache.thrift.scheme.IScheme;
import org.apache.thrift.scheme.SchemeFactory;
import org.apache.thrift.scheme.StandardScheme;

import org.apache.thrift.scheme.TupleScheme;
import org.apache.thrift.protocol.TTupleProtocol;
import org.apache.thrift.protocol.TProtocolException;
import org.apache.thrift.EncodingUtils;
import org.apache.thrift.TException;
import org.apache.thrift.async.AsyncMethodCallback;
import org.apache.thrift.server.AbstractNonblockingServer.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.EnumMap;
import java.util.Set;
import java.util.HashSet;
import java.util.EnumSet;
import java.util.Collections;
import java.util.BitSet;
import java.nio.ByteBuffer;
import java.util.Arrays;
import javax.annotation.Generated;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Generated(value = "Autogenerated by Frugal Compiler (1.18.0)", date = "2015-11-24")
public class thing implements org.apache.thrift.TBase<thing, thing._Fields>, java.io.Serializable, Cloneable, Comparable<thing> {
	private static final org.apache.thrift.protocol.TStruct STRUCT_DESC = new org.apache.thrift.protocol.TStruct("thing");

	private static final org.apache.thrift.protocol.TField AN_ID_FIELD_DESC = new org.apache.thrift.protocol.TField("an_id", org.apache.thrift.protocol.TType.I32, (short)1);
	private static final org.apache.thrift.protocol.TField A_STRING_FIELD_DESC = new org.apache.thrift.protocol.TField("a_string", org.apache.thrift.protocol.TType.STRING, (short)2);

	private static final Map<Class<? extends IScheme>, SchemeFactory> schemes = new HashMap<Class<? extends IScheme>, SchemeFactory>();
	static {
		schemes.put(StandardScheme.class, new thingStandardSchemeFactory());
		schemes.put(TupleScheme.class, new thingTupleSchemeFactory());
	}

	public int an_id; // required
	public String a_string; // required
	/** The set of fields this struct contains, along with convenience methods for finding and manipulating them. */
	public enum _Fields implements org.apache.thrift.TFieldIdEnum {
		AN_ID((short)1, "an_id"),
		A_STRING((short)2, "a_string")
;

		private static final Map<String, _Fields> byName = new HashMap<String, _Fields>();

		static {
			for (_Fields field : EnumSet.allOf(_Fields.class)) {
				byName.put(field.getFieldName(), field);
			}
		}

		/**
		 * Find the _Fields constant that matches fieldId, or null if its not found.
		 */
		public static _Fields findByThriftId(int fieldId) {
			switch(fieldId) {
				case 1: // AN_ID
					return AN_ID;
				case 2: // A_STRING
					return A_STRING;
				default:
					return null;
			}
		}

		/**
		 * Find the _Fields constant that matches fieldId, throwing an exception
		 * if it is not found.
		 */
		public static _Fields findByThriftIdOrThrow(int fieldId) {
			_Fields fields = findByThriftId(fieldId);
			if (fields == null) throw new IllegalArgumentException("Field " + fieldId + " doesn't exist!");
			return fields;
		}

		/**
		 * Find the _Fields constant that matches name, or null if its not found.
		 */
		public static _Fields findByName(String name) {
			return byName.get(name);
		}

		private final short _thriftId;
		private final String _fieldName;

		_Fields(short thriftId, String fieldName) {
			_thriftId = thriftId;
			_fieldName = fieldName;
		}

		public short getThriftFieldId() {
			return _thriftId;
		}

		public String getFieldName() {
			return _fieldName;
		}
	}

	// isset id assignments
	private static final int __AN_ID_ISSET_ID = 0;
	private byte __isset_bitfield = 0;
	public static final Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> metaDataMap;
	static {
		Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> tmpMap = new EnumMap<_Fields, org.apache.thrift.meta_data.FieldMetaData>(_Fields.class);
		tmpMap.put(_Fields.AN_ID, new org.apache.thrift.meta_data.FieldMetaData("an_id", org.apache.thrift.TFieldRequirementType.DEFAULT,
				new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.I32)));
		tmpMap.put(_Fields.A_STRING, new org.apache.thrift.meta_data.FieldMetaData("a_string", org.apache.thrift.TFieldRequirementType.DEFAULT,
				new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
		metaDataMap = Collections.unmodifiableMap(tmpMap);
		org.apache.thrift.meta_data.FieldMetaData.addStructMetaDataMap(thing.class, metaDataMap);
	}

	public thing() {
	}

	public thing(
		int an_id,
		String a_string) {
		this();
		this.an_id = an_id;
		setAn_idIsSet(true);
		this.a_string = a_string;
	}

	/**
	 * Performs a deep copy on <i>other</i>.
	 */
	public thing(thing other) {
		__isset_bitfield = other.__isset_bitfield;
		this.an_id = other.an_id;
		if (other.isSetA_string()) {
			this.a_string = other.a_string;
		}
	}

	public thing deepCopy() {
		return new thing(this);
	}

	@Override
	public void clear() {
		setAn_idIsSet(false);
		this.an_id = 0;

		this.a_string = null;

	}

	public int getAn_id() {
		return this.an_id;
	}

	public thing setAn_id(int an_id) {
		this.an_id = an_id;
		setAn_idIsSet(true);
		return this;
	}

	public void unsetAn_id() {
		__isset_bitfield = EncodingUtils.clearBit(__isset_bitfield, __AN_ID_ISSET_ID);
	}

	/** Returns true if field an_id is set (has been assigned a value) and false otherwise */
	public boolean isSetAn_id() {
		return EncodingUtils.testBit(__isset_bitfield, __AN_ID_ISSET_ID);
	}

	public void setAn_idIsSet(boolean value) {
		__isset_bitfield = EncodingUtils.setBit(__isset_bitfield, __AN_ID_ISSET_ID, value);
	}

	public String getA_string() {
		return this.a_string;
	}

	public thing setA_string(String a_string) {
		this.a_string = a_string;
		return this;
	}

	public void unsetA_string() {
		this.a_string = null;
	}

	/** Returns true if field a_string is set (has been assigned a value) and false otherwise */
	public boolean isSetA_string() {
		return this.a_string != null;
	}

	public void setA_stringIsSet(boolean value) {
		if (!value) {
			this.a_string = null;
		}
	}

	public void setFieldValue(_Fields field, Object value) {
		switch (field) {
		case AN_ID:
			if (value == null) {
				unsetAn_id();
			} else {
				setAn_id((Integer)value);
			}
			break;

		case A_STRING:
			if (value == null) {
				unsetA_string();
			} else {
				setA_string((String)value);
			}
			break;

		}
	}

	public Object getFieldValue(_Fields field) {
		switch (field) {
		case AN_ID:
			return getAn_id();

		case A_STRING:
			return getA_string();

		}
		throw new IllegalStateException();
	}

	/** Returns true if field corresponding to fieldID is set (has been assigned a value) and false otherwise */
	public boolean isSet(_Fields field) {
		if (field == null) {
			throw new IllegalArgumentException();
		}

		switch (field) {
		case AN_ID:
			return isSetAn_id();
		case A_STRING:
			return isSetA_string();
		}
		throw new IllegalStateException();
	}

	@Override
	public boolean equals(Object that) {
		if (that == null)
			return false;
		if (that instanceof thing)
			return this.equals((thing)that);
		return false;
	}

	public boolean equals(thing that) {
		if (that == null)
			return false;

		boolean this_present_an_id = true;
		boolean that_present_an_id = true;
		if (this_present_an_id || that_present_an_id) {
			if (!(this_present_an_id && that_present_an_id))
				return false;
			if (this.an_id != that.an_id)
				return false;
		}

		boolean this_present_a_string = true && this.isSetA_string();
		boolean that_present_a_string = true && that.isSetA_string();
		if (this_present_a_string || that_present_a_string) {
			if (!(this_present_a_string && that_present_a_string))
				return false;
			if (!this.a_string.equals(that.a_string))
				return false;
		}

		return true;
	}

	@Override
	public int hashCode() {
		List<Object> list = new ArrayList<Object>();

		boolean present_an_id = true;
		list.add(present_an_id);
		if (present_an_id)
			list.add(an_id);

		boolean present_a_string = true && (isSetA_string());
		list.add(present_a_string);
		if (present_a_string)
			list.add(a_string);

		return list.hashCode();
	}

	@Override
	public int compareTo(thing other) {
		if (!getClass().equals(other.getClass())) {
			return getClass().getName().compareTo(other.getClass().getName());
		}

		int lastComparison = 0;

		lastComparison = Boolean.valueOf(isSetAn_id()).compareTo(other.isSetAn_id());
		if (lastComparison != 0) {
			return lastComparison;
		}
		if (isSetAn_id()) {
			lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.an_id, other.an_id);
			if (lastComparison != 0) {
				return lastComparison;
			}
		}
		lastComparison = Boolean.valueOf(isSetA_string()).compareTo(other.isSetA_string());
		if (lastComparison != 0) {
			return lastComparison;
		}
		if (isSetA_string()) {
			lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.a_string, other.a_string);
			if (lastComparison != 0) {
				return lastComparison;
			}
		}
		return 0;
	}

	public _Fields fieldForId(int fieldId) {
		return _Fields.findByThriftId(fieldId);
	}

	public void read(org.apache.thrift.protocol.TProtocol iprot) throws org.apache.thrift.TException {
		schemes.get(iprot.getScheme()).getScheme().read(iprot, this);
	}

	public void write(org.apache.thrift.protocol.TProtocol oprot) throws org.apache.thrift.TException {
		schemes.get(oprot.getScheme()).getScheme().write(oprot, this);
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder("thing(");
		boolean first = true;

		sb.append("an_id:");
		sb.append(this.an_id);
		first = false;
		if (!first) sb.append(", ");
		sb.append("a_string:");
		if (this.a_string == null) {
			sb.append("null");
		} else {
			sb.append(this.a_string);
		}
		first = false;
		sb.append(")");
		return sb.toString();
	}

	public void validate() throws org.apache.thrift.TException {
		// check for required fields
		// check for sub-struct validity
	}

	private void writeObject(java.io.ObjectOutputStream out) throws java.io.IOException {
		try {
			write(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(out)));
		} catch (org.apache.thrift.TException te) {
			throw new java.io.IOException(te);
		}
	}

	private void readObject(java.io.ObjectInputStream in) throws java.io.IOException, ClassNotFoundException {
		try {
			// it doesn't seem like you should have to do this, but java serialization is wacky, and doesn't call the default constructor.
			__isset_bitfield = 0;
			read(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(in)));
		} catch (org.apache.thrift.TException te) {
			throw new java.io.IOException(te);
		}
	}

	private static class thingStandardSchemeFactory implements SchemeFactory {
		public thingStandardScheme getScheme() {
			return new thingStandardScheme();
		}
	}

	private static class thingStandardScheme extends StandardScheme<thing> {

		public void read(org.apache.thrift.protocol.TProtocol iprot, thing struct) throws org.apache.thrift.TException {
			org.apache.thrift.protocol.TField schemeField;
			iprot.readStructBegin();
			while (true) {
				schemeField = iprot.readFieldBegin();
				if (schemeField.type == org.apache.thrift.protocol.TType.STOP) {
					break;
				}
				switch (schemeField.id) {
					case 1: // AN_ID
						if (schemeField.type == org.apache.thrift.protocol.TType.I32) {
							struct.an_id = iprot.readI32();
							struct.setAn_idIsSet(true);
						} else {
							org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
						}
						break;
					case 2: // A_STRING
						if (schemeField.type == org.apache.thrift.protocol.TType.STRING) {
							struct.a_string = iprot.readString();
							struct.setA_stringIsSet(true);
						} else {
							org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
						}
						break;
					default:
						org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
				}
				iprot.readFieldEnd();
			}
			iprot.readStructEnd();

			// check for required fields of primitive type, which can't be checked in the validate method
			struct.validate();
		}

		public void write(org.apache.thrift.protocol.TProtocol oprot, thing struct) throws org.apache.thrift.TException {
			struct.validate();

			oprot.writeStructBegin(STRUCT_DESC);
			oprot.writeFieldBegin(AN_ID_FIELD_DESC);
			oprot.writeI32(struct.an_id);
			oprot.writeFieldEnd();
			if (struct.a_string != null) {
				oprot.writeFieldBegin(A_STRING_FIELD_DESC);
				oprot.writeString(struct.a_string);
				oprot.writeFieldEnd();
			}
			oprot.writeFieldStop();
			oprot.writeStructEnd();
		}

	}

	private static class thingTupleSchemeFactory implements SchemeFactory {
		public thingTupleScheme getScheme() {
			return new thingTupleScheme();
		}
	}

	private static class thingTupleScheme extends TupleScheme<thing> {

		@Override
		public void write(org.apache.thrift.protocol.TProtocol prot, thing struct) throws org.apache.thrift.TException {
			TTupleProtocol oprot = (TTupleProtocol) prot;
			BitSet optionals = new BitSet();
			if (struct.isSetAn_id()) {
				optionals.set(0);
			}
			if (struct.isSetA_string()) {
				optionals.set(1);
			}
			oprot.writeBitSet(optionals, 2);
			if (struct.isSetAn_id()) {
				oprot.writeI32(struct.an_id);
			}
			if (struct.isSetA_string()) {
				oprot.writeString(struct.a_string);
			}
		}

		@Override
		public void read(org.apache.thrift.protocol.TProtocol prot, thing struct) throws org.apache.thrift.TException {
			TTupleProtocol iprot = (TTupleProtocol) prot;
			BitSet incoming = iprot.readBitSet(2);
			if (incoming.get(0)) {
				struct.an_id = iprot.readI32();
				struct.setAn_idIsSet(true);
			}
			if (incoming.get(1)) {
				struct.a_string = iprot.readString();
				struct.setA_stringIsSet(true);
			}
		}

	}

}
