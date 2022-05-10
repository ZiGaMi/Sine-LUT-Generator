# ===============================================================================
# @file:    sine_lut_gen.py
# @note:    This sript generated sine LUT 
# @author:  Ziga Miklosic
# @date:    28.04.2022
# @version: V0.1.0
# @brief:   This script generated sine look-up table based on 
#           specific settings inputed. It outputs C generated code of
#           LUT generation
# ===============================================================================

# ===============================================================================
#       IMPORTS  
# ===============================================================================
import os
import numpy as np
import matplotlib.pyplot as plt

# ===============================================================================
#       CONSTANTS
# ===============================================================================

# Sript version
SCRIPT_VER = "V0.1.0"

# Number of elements in LUT
N = 1024

# DAC resolution ( in bits )
DAC_RES = 12	

# DAC Vref
DAC_VREF = 2.5  #V

# Sine DC offset
SIN_DC = 1.0    # V

# Sine amplitude
SIN_AMP = 0.9   # V

# Sine phase
SIN_PHASE = 0 # rad

# Show graphs at the end
GRAPH_EN = True

# ===============================================================================
#       FUNCTIONS
# ===============================================================================

# ===============================================================================
# @brief:  Write comment to output generated file
#
# @param[in]:   file            - File that result will be putted
# @param[in]:   size_of_element - Size of value inside LUT
# @return:      void
# ===============================================================================
def write_c_comment(file, size_of_element):
    file.write( "/**\n" );
    file.write( " *    Sine LUT table\n" );
    file.write( " *\n" );
    file.write( " * @note   This table is automatically generated with a help of\n" );
    file.write( " *         sine_lut_gen.py python script version %s\n" % SCRIPT_VER );
    file.write( " *\n" );
    file.write( " *         Script can be found under /utils directory\n" );
    file.write( " *\n" );
    file.write( " *     Size of LUT in bytes: %s\n" % ( size_of_element * N ));
    file.write( " *\n" );
    file.write( " *     Generated sine signal property:\n" );
    file.write( " *       - DC-offset = %s V\n" % SIN_DC );
    file.write( " *       - Amplitude = %s V\n" % SIN_AMP );
    file.write( " *       - Phase = %s rad\n" % SIN_PHASE );
    file.write( " */\n" );

# ===============================================================================
# @brief:  Write header
#
# @param[in]:   file            - File that result will be putted
# @return:      void
# ===============================================================================
def write_header(file):

    if DAC_RES <= 8:
        write_c_comment( file, 1 );
        file.write( "const uint8_t gu8_sin_lut[%s] = {" % N )
   
    elif DAC_RES <= 16:
        write_c_comment( file, 2 );
        file.write( "const uint16_t gu16_sin_lut[%s] = {" % N )
    
    elif DAC_RES <= 32:  
        write_c_comment( file, 4 );
        file.write( "const uint32_t gu32_sin_lut[%s] = {" % N )

# ===============================================================================
# @brief:  Main entry function
#
# @return:       void
# ===============================================================================
def main():

    sin_lut = []
    lut_idx_plt = []
    theta_plt = []
    theta = 0           # Angle in rad
    sin_real_plot = []

    # Open file
    out_file = open( "sin_lut.txt", "w")

    # Write header output file
    write_header( out_file )

    # Generate table
    for i in range( N ):

        # Calculate real sine signal
        sin_real = ( SIN_AMP * np.sin( theta + SIN_PHASE )) + SIN_DC 

        # Calculate raw sine signal
        sin_raw = int((( 2**DAC_RES ) - 1 ) * ( sin_real / DAC_VREF ))

        # Increase angle
        theta += ( 2 * np.pi / N )

        # Fill array
        sin_lut.append( sin_raw )

        # Add to plot
        theta_plt.append( theta )
        sin_real_plot.append(sin_real)
        lut_idx_plt.append( i )
        
        # Put new line after 16th value
        if 0 == i % 16:
            out_file.write( "\n    " )

        # Last number
        if i == ( N-1 ): 
            out_file.write( "%s " % str(sin_raw) )
        else:
            out_file.write( "%s, " % str(sin_raw) )

    out_file.write( "\n};" )
    out_file.write( "" )

    if GRAPH_EN:
        # =============================================================================================
        ## PLOT CONFIGURATIONS
        # =============================================================================================
        plt.style.use(['dark_background'])
        PLOT_SIZE_INCHES        = ( 16, 9 )
        PLOT_MAIN_TITLE_SIZE    = 16
        PLOT_MAIN_TITLE         = "Sine LUT generation N: " + str(N)
        PLOT_TITLE_SIZE         = 16
        PLOT_AXIS_LABEL_SIZE    = 14
        PLOT_ADJUST_LEFT        = 0.055
        PLOT_ADJUST_RIGHT       = 0.967
        PLOT_ADJUST_TOP         = 0.9
        PLOT_ADJUST_BOTTOM      = 0.055
        PLOT_ADJUST_HSPACE      = 0.283
        PLOT_ADJUST_WSPACE      = 0.164

        # Figure
        fig, ( ax1, ax2 ) = plt.subplots( 2, 1, sharex=False )
        fig.suptitle( PLOT_MAIN_TITLE , fontsize=PLOT_MAIN_TITLE_SIZE )
        fig.set_size_inches( PLOT_SIZE_INCHES )
        plt.subplots_adjust(left=PLOT_ADJUST_LEFT, right=PLOT_ADJUST_RIGHT, top=PLOT_ADJUST_TOP, bottom=PLOT_ADJUST_BOTTOM, hspace=PLOT_ADJUST_HSPACE, wspace=PLOT_ADJUST_WSPACE)
        
        # Plot
        ax1.set_title("Real ", fontsize=PLOT_TITLE_SIZE )
        ax1.plot( theta_plt, sin_real_plot, "r" )
        ax1.grid(alpha=0.25)
        ax1.set_ylabel('Real DAC values',   fontsize=PLOT_AXIS_LABEL_SIZE )
        ax1.set_xlabel('Theta [rad]',       fontsize=PLOT_AXIS_LABEL_SIZE )

        ax2.set_title("LUT", fontsize=PLOT_TITLE_SIZE)
        ax2.plot( lut_idx_plt, sin_lut, "r-o" )
        ax2.grid(alpha=0.25)
        ax2.set_xlabel('LUT index'          , fontsize=PLOT_AXIS_LABEL_SIZE )
        ax2.set_ylabel('Raw DAC values'     ,fontsize=PLOT_AXIS_LABEL_SIZE )
        
        plt.show()

# ===============================================================================
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================