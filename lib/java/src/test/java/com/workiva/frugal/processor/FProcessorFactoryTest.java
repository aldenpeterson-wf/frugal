package com.workiva.frugal.processor;

import org.apache.thrift.transport.TTransport;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;

/**
 * Tests for {@link FProcessorFactory}.
 */
@RunWith(JUnit4.class)
public class FProcessorFactoryTest {

    @Test
    public void testGetFProcessor() throws Exception {

        FProcessor expected = mock(FProcessor.class);

        FProcessorFactory factory = new FProcessorFactory(expected);

        FProcessor actual = factory.getProcessor(mock(TTransport.class));

        assertEquals(expected, actual);
    }
}
