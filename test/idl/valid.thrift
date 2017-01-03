namespace java foo

include "excepts.thrift"

include "validStructs.thrift"

include "ValidTypes.thrift"

/**
 * This is a docstring.
 */
struct Thing {
	1: i32 bar,
	2: i32 baz,
	3: i32 qux,
}

struct Stuff {
}

typedef i32 Int

exception InvalidOperation {
	1: i32 whatOp,
	2: string why,
}

/**
 * This is a service docstring.
 */
service Blah {
	/**
	 * Use this to ping the server.
	 */
	void ping(),

	/**
	 * Use this to tell the server how you feel.
	 */
	i64 bleh(1: Thing one, 2: Stuff Two, 3: list<Int> custom_ints) throws (1:InvalidOperation oops, 2:excepts.InvalidData err2),

	validStructs.Thing getThing(),

	ValidTypes.MyInt getMyInt(),

}

