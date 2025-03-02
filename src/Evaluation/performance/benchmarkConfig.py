import subprocess

"""
1. formats/raw.pl is corrupted! 是路径带来的问题！！  另外目前看起来最好的版本是1.1.8，这个要保留下来
rm -Rf /E/dataset/specpu/benchspec/CPU/*/run
rm -Rf /E/dataset/specpu/benchspec/CPU/*/exe
rm -Rf /E/dataset/specpu/benchspec/CPU/*/orig
rm -Rf /E/dataset/specpu/benchspec/CPU/*/random
rm -Rf /E/dataset/specpu/benchspec/CPU/*/build

rm -Rf ../benchspec/CPU/*/run
rm -Rf ../benchspec/CPU/*/exe
rm -Rf ../benchspec/CPU/*/build

./runcpu --action=build --rebuild --config=clang15-myhwasan-arm64-O3 intspeed intrate
./runcpu --action=build --rebuild --config=clang15-hwasan-arm64-O3 intspeed intrate
./runcpu --action=build --rebuild --config=clang15-orig-arm64-O3 intspeed intrate

./runcpu --action=build --rebuild --config=np-x64-O3 intrate intspeed fprate fpspeed 541.leela_r 510.parest_r 521.wrf_r 641.leela_s 623.xalancbmk_s 657.xz_s 511.povray_r 627.cam4_s
./runcpu --action=build --rebuild --config=np-x64-O3 511.povray_r 523.xalancbmk_r
./runcpu --action=runsetup --config=np-x64-O3 511.povray_r 523.xalancbmk_r

./runcpu --action=build --rebuild --config=np-arm64-O3-multirandom intrate intspeed fprate fpspeed

./runcpu --action=build --rebuild --config=gcc9-np-arm64-O0 intrate fprate
./runcpu --action=build --rebuild --config=gcc9-np-arm64-O1 intrate fprate
./runcpu --action=build --rebuild --config=gcc9-np-arm64-O3 intrate fprate
./runcpu --action=build --rebuild --config=gcc9-np-arm64-Of intrate fprate
./runcpu --action=build --rebuild --config=gcc9-np-arm64-Os intrate fprate
./runcpu --action=build --rebuild --config=gcc9-np-arm64-O3-pie intrate fprate
./runcpu --action=build --rebuild --config=gcc10-np-arm64-O3-large intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-O0 intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-O1 intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-O3 intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-Os intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-Of intrate fprate
./runcpu --action=build --rebuild --config=clang10-np-arm64-O3-pie intrate fprate
easy to false: fpspeed  510.parest_r 521.wrf_r 623.xalancbmk_s

2. python3.10 /ccr/randomizer/NoCompiler/performanceEvaluation/extractSpeccmd.py

3. python3.10 /ccr/randomizer/NoCompiler/performanceEvaluation/generateBenchmarkVariant.py run 4
   python3.10 /ccr/randomizer/NoCompiler/performanceEvaluation/generateBenchmarkVariant.py performance 10

4. python3.10 /ccr/randomizer/NoCompiler/performanceEvaluation/runBenchmark.py fun run 3
./runcpu --action=run --config=ccx-x64-O3 541.leela_r 510.parest_r 521.wrf_r 641.leela_s 623.xalancbmk_s 657.xz_s 511.povray_r 627.cam4_s
./runcpu --action=run --config=ccx-arm64-O3 627.cam4_s 641.leela_s 657.xz_s 511.povray_r 654.roms_s 603.bwaves_s 510.parest_r 620.omnetpp_s


echo root | sudo -S ld.sh np-arm64
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed

echo root | sudo -S ld.sh orig-arm64
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
./runcpu --action=build --rebuild --config=gcc7-np-arm64-O3 intrate intspeed fprate fpspeed
ls

"""

pranderPath = "/ccr/randomizer/NoCompiler/prander.py"
specinvoke = "/E/dataset/specpu/bin/specinvoke"
readelf = "readelf"
root = "/E/dataset/specpu/benchspec/CPU/"

retu = subprocess.run(args=["uname -a"], shell=True, capture_output=True)




if b"aarch64" in retu.stdout:
    """
    """

    config = "np-arm64-O3"
    suffix = "np-arm64-O3"

    runPathList = ['/E/dataset/specpu/benchspec/CPU/531.deepsjeng_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/526.blender_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/548.exchange2_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/998.specrand_is/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/649.fotonik3d_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/638.imagick_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/628.pop2_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/523.xalancbmk_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/505.mcf_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/600.perlbench_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/508.namd_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/625.x264_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/999.specrand_ir/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/623.xalancbmk_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/621.wrf_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/544.nab_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/510.parest_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/503.bwaves_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/620.omnetpp_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/502.gcc_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/549.fotonik3d_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/507.cactuBSSN_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/538.imagick_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/511.povray_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/603.bwaves_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/519.lbm_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/631.deepsjeng_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/607.cactuBSSN_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/605.mcf_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/997.specrand_fr/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/527.cam4_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/520.omnetpp_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/541.leela_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/554.roms_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/557.xz_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/657.xz_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/644.nab_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/648.exchange2_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/500.perlbench_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/654.roms_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/996.specrand_fs/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/602.gcc_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/619.lbm_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/641.leela_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/525.x264_r/run/run_base_refrate_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/627.cam4_s/run/run_base_refspeed_np-arm64-O3-64.0000',
                   '/E/dataset/specpu/benchspec/CPU/521.wrf_r/run/run_base_refrate_np-arm64-O3-64.0000']

    failedRunPath = [
"""
/E/dataset/specpu/benchspec/CPU/649.fotonik3d_s/run/run_base_refspeed_np-arm64-O3-64.0000 137
/E/dataset/specpu/benchspec/CPU/603.bwaves_s/run/run_base_refspeed_np-arm64-O3-64.0000 137
/E/dataset/specpu/benchspec/CPU/631.deepsjeng_s/run/run_base_refspeed_np-arm64-O3-64.0000 137
/E/dataset/specpu/benchspec/CPU/654.roms_s/run/run_base_refspeed_np-arm64-O3-64.0000 137
"""

    ]





else:
    """
    """

    config = "np-x64-O3"
    readelf = "readelf"
    suffix = "np-x64-O3"

    runPathList = [
        '/E/dataset/specpu/benchspec/CPU/511.povray_r/run/run_base_refrate_np-x64-O3-m64.0000',
        '/E/dataset/specpu/benchspec/CPU/523.xalancbmk_r/run/run_base_refrate_np-x64-O3-m64.0000'
    ]

    failedRunPath = [
        ""
    ]




#whiteList = ['998.specrand_is', '523.xalancbmk_r', '531.deepsjeng_r', '620.omnetpp_s', '507.cactuBSSN_r', '525.x264_r', '503.bwaves_r', '541.leela_r', '557.xz_r', '649.fotonik3d_s', '527.cam4_r', '510.parest_r', '648.exchange2_s', '625.x264_s', '538.imagick_r', '502.gcc_r', '526.blender_r', '544.nab_r', '505.mcf_r', '654.roms_s', '644.nab_s', '607.cactuBSSN_s', '641.leela_s', '997.specrand_fr', '548.exchange2_r', '631.deepsjeng_s', '500.perlbench_r', '521.wrf_r', '605.mcf_s', '996.specrand_fs', '603.bwaves_s', '600.perlbench_s', '619.lbm_s', '549.fotonik3d_r', '602.gcc_s', '628.pop2_s', '520.omnetpp_r', '519.lbm_r', '623.xalancbmk_s', '657.xz_s', '999.specrand_ir', '511.povray_r', '627.cam4_s', '508.namd_r', '554.roms_r', '638.imagick_s']
