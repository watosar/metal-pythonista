/*
See LICENSE folder for this sample’s licensing information.

Abstract:
Metal shaders used for this sample
*/

#include <metal_stdlib>
#include <simd/simd.h>

using namespace metal;

typedef struct{
    float4 position [[position]];
    
    float4 color;
    
} RasterizerData;


vertex RasterizerData vertexShader(
    uint vertexID [[vertex_id]]
){

    RasterizerData out;
    float pi = 3.1415;
    out.position = float4(sin(pi*0.6666*vertexID), cos(pi*0.6666*vertexID)-0.2, 0.0, 1.0);
    
    if (vertexID == 0){
        out.color = float4(1.0,0.5,0.0,0.0);
    }
    else if (vertexID == 1){
        out.color = float4(0.0,1.0,0.5,0.0);
    }
    else if (vertexID == 2){
        out.color = float4(0.5,0.0,1.0,0.1);
    }
    
    
    return out;
    
}


fragment float4 fragmentShader(

    RasterizerData in [[stage_in]],
    constant float *_time [[buffer(0)]]
    
){
    return in.color;
    
}