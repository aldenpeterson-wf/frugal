// Autogenerated by Frugal Compiler (1.14.0)
// DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING

library music.src.f_album;

import 'dart:typed_data' show Uint8List;
import 'package:thrift/thrift.dart';
import 'package:v1.music/v1.music.dart' as t_v1.music;

/// The IDL provides set, list, and map types for representing collections
/// of data.  Our Album struct contains a list of Tracks.
class Album implements TBase {
  static final TStruct _STRUCT_DESC = new TStruct("Album");
  static final TField _TRACKS_FIELD_DESC = new TField("tracks", TType.LIST, 1);
  static final TField _DURATION_FIELD_DESC = new TField("duration", TType.DOUBLE, 2);
  static final TField _ASIN_FIELD_DESC = new TField("ASIN", TType.STRING, 3);

  List<t_v1.music.Track> _tracks;
  static const int TRACKS = 1;
  double _duration;
  static const int DURATION = 2;
  String _aSIN;
  static const int ASIN = 3;

  bool __isset_duration = false;

  Album() {
  }

  List<t_v1.music.Track> get tracks => this._tracks;

  set tracks(List<t_v1.music.Track> tracks) {
    this._tracks = tracks;
  }

  bool isSetTracks() => this.tracks != null;

  unsetTracks() {
    this.tracks = null;
  }

  double get duration => this._duration;

  set duration(double duration) {
    this._duration = duration;
    this.__isset_duration = true;
  }

  bool isSetDuration() => this.__isset_duration;

  unsetDuration() {
    this.__isset_duration = false;
  }

  String get aSIN => this._aSIN;

  set aSIN(String aSIN) {
    this._aSIN = aSIN;
  }

  bool isSetASIN() => this.aSIN != null;

  unsetASIN() {
    this.aSIN = null;
  }

  getFieldValue(int fieldID) {
    switch (fieldID) {
      case TRACKS:
        return this.tracks;
      case DURATION:
        return this.duration;
      case ASIN:
        return this.aSIN;
      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  setFieldValue(int fieldID, Object value) {
    switch(fieldID) {
      case TRACKS:
        if(value == null) {
          unsetTracks();
        } else {
          this.tracks = value;
        }
        break;

      case DURATION:
        if(value == null) {
          unsetDuration();
        } else {
          this.duration = value;
        }
        break;

      case ASIN:
        if(value == null) {
          unsetASIN();
        } else {
          this.aSIN = value;
        }
        break;

      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  // Returns true if the field corresponding to fieldID is set (has been assigned a value) and false otherwise
  bool isSet(int fieldID) {
    switch(fieldID) {
      case TRACKS:
        return isSetTracks();
      case DURATION:
        return isSetDuration();
      case ASIN:
        return isSetASIN();
      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  read(TProtocol iprot) {
    TField field;
    iprot.readStructBegin();
    while(true) {
      field = iprot.readFieldBegin();
      if(field.type == TType.STOP) {
        break;
      }
      switch(field.id) {
        case TRACKS:
          if(field.type == TType.LIST) {
            TList elem0 = iprot.readListBegin();
            tracks = new List<t_v1.music.Track>();
            for(int elem2 = 0; elem2 < elem0.length; ++elem2) {
              t_v1.music.Track elem1 = new t_v1.music.Track();
              elem1.read(iprot);
              tracks.add(elem1);
            }
            iprot.readListEnd();
          } else {
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case DURATION:
          if(field.type == TType.DOUBLE) {
            duration = iprot.readDouble();
            this.__isset_duration = true;
          } else {
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case ASIN:
          if(field.type == TType.STRING) {
            aSIN = iprot.readString();
          } else {
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        default:
          TProtocolUtil.skip(iprot, field.type);
          break;
      }
      iprot.readFieldEnd();
    }
    iprot.readStructEnd();

    // check for required fields of primitive type, which can't be checked in the validate method
    validate();
  }

  write(TProtocol oprot) {
    validate();

    oprot.writeStructBegin(_STRUCT_DESC);
    if(this.tracks != null) {
      oprot.writeFieldBegin(_TRACKS_FIELD_DESC);
      oprot.writeListBegin(new TList(TType.STRUCT, tracks.length));
      for(var elem3 in tracks) {
        elem3.write(oprot);
      }
      oprot.writeListEnd();
      oprot.writeFieldEnd();
    }
    oprot.writeFieldBegin(_DURATION_FIELD_DESC);
    oprot.writeDouble(duration);
    oprot.writeFieldEnd();
    if(this.aSIN != null) {
      oprot.writeFieldBegin(_ASIN_FIELD_DESC);
      oprot.writeString(aSIN);
      oprot.writeFieldEnd();
    }
    oprot.writeFieldStop();
    oprot.writeStructEnd();
  }

  String toString() {
    StringBuffer ret = new StringBuffer("Album(");

    ret.write("tracks:");
    if(this.tracks == null) {
      ret.write("null");
    } else {
      ret.write(this.tracks);
    }

    ret.write(", ");
    ret.write("duration:");
    ret.write(this.duration);

    ret.write(", ");
    ret.write("aSIN:");
    if(this.aSIN == null) {
      ret.write("null");
    } else {
      ret.write(this.aSIN);
    }

    ret.write(")");

    return ret.toString();
  }

  validate() {
    // check for required fields
    // check that fields of type enum have valid values
  }
}
