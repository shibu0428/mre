//you can call send_lorawan_pkt(deveui,data,port) to send data to node through local lorawan server
//callback prototype 
//- function onInit() {}
//- function onLoRaWANRx(message){ }
//- function onLoRaRx (data) {}
//you can call debug_print(msg) to print log
//you can call send_pkt(data) to forward data
function onInit() {
    debug_print("on init");  
  }
  
  function onLoRaRx (data) {
    debug_print("on Recv data");
    debug_print(data);
  }
  
  function onLoRaWANRx(message){
      
      const data=JSON.parse(JSON.stringify(message));
      
      const deveui=data.deveui;
      const devname=data.devname;
      const raw_data=data.raw_data;
      const fport=data.fport;
      
      if(fport<=3){
          const send_data=loraDecoder(deveui,devname,raw_data,fport);
          debug_print(JSON.stringify(send_data));
      }
  }
  
  ////////////////////////////////////////////////////
  //
  // decorderの読込
  //
  ////////////////////////////////////////////////////
  
  //
  // 新規作成関数
  //
  function loraDecoder(deveui, devname, rowData, port) {
      
      var decodedFields, propNames, str;
      var bytes = [];
  
      // 送信タイムスタンプ
      const timestamp = new Date().toISOString();
      
      for (var i = 0; i < rowData.length / 2; i++) {
          str = rowData.substr(i * 2, 2);
          if (str.length < 2) break;
          bytes[i] = hex2dec(str, 1);
      }
  
      decodedFields = Decoder(bytes, port);
      
      // 配列の初期化
      // const dataArr = [];         // 送信データ
      const dataObj = {
          timestamp: timestamp,
          id: deveui,
          device: devname,
          payload: decodedFields,
      }
      
      // // 送信データのJSON
      // // dataArr.push({
      // //     timestamp: timestamp,
      // //     id: deveui,
      // //     device: devname,
      // //     payload: decodedFields,
      // // });
      //     dataArr.push({
      //     timestamp: timestamp,
      //     id: deveui,
      //     device: devname,
      //     payload: decodedFields,
      // });
      // return dataArr;
      return dataObj;
  }
  
  //
  // 以下はDeltaOhm提供スクリプト
  //
  
  var measSetVect = [];
  measSetVect[0] = [
      { title: "temperature", res: 1, unit: 0 }, //0 0.1 °C
      { title: "relative_humidity", res: 1, unit: 2 }, //1 0.1 %
      { title: "dew_point", res: 1, unit: 0 }, //2 0.1 °C
      { title: "partial_vapor_pressure", res: 2, unit: 8 }, //3 0.01 hPa
      { title: "mixing_ratio", res: 1, unit: 4 }, //4 0.1 g/kg
      { title: "absolute_humidity", res: 1, unit: 3 }, //5 0.1 g/m3
      { title: "wet_point", res: 1, unit: 0 }, //6 0.1 °C
      { title: "differential_pressure", res: 1, unit: 8 }, //7 0.1 hPa
      { title: "temperature", res: 1, unit: 0 }, //8 0.1 °C
      { title: "solar_radiation", res: 0, unit: 22 }, //9 1 W/m2
      { title: "illuminance", res: 0, unit: 35 }, //10 1 LUX
      { title: "carbon_monoxide", res: 0, unit: 31 }, //11 1 ppm
      { title: "atmospheric_pressure", res: 1, unit: 5 }, //12 0.1 mbar
      { title: "frequency", res: 0, unit: 32 }, //13 1 Hz
      { title: "mapped_frequency", res: 0, unit: 255 }, //14 1 not def
      { title: "daily_global_radiation", res: 0, unit: 24 }, //15 1 Wh/m2
      { title: "carbon_dioxide", res: 0, unit: 31 }, //16 1 ppm
      { title: "volumetric_water_content", res: 1, unit: 2 }, //17 0.1 %
      { title: "soil_moisture", res: 1, unit: 29 }, //18 0.1 mV
      { title: "acceleration_z", res: 3, unit: 37 }, //19 0.001 g
      { title: "height", res: 0, unit: 45 }, //20 1 m
      { title: "shock_time", res: 2, unit: 46 }, //21 0.01 sec
      { title: "delta_speed", res: 1, unit: 17 }, //22 0.1 m/s
      { title: "temperature", res: 1, unit: 0 }, //23 0.1 °C
      { title: "relative_humidity", res: 1, unit: 2 }, //24 0.1 %
      { title: "temperature", res: 1, unit: 0 }, //25 0.1 °C
      { title: "wind_speed", res: 1, unit: 17 }, //26 0.1 m/s
      { title: "wind_direction", res: 0, unit: 34 }, //27 1 DEG
      { title: "differential_pressure", res: 0, unit: 7 }, //28 1 Pa
      { title: "wind_chill", res: 1, unit: 0 }, //29 0.1 °C
      { title: "differential_pressure", res: 1, unit: 7 }, //30 0.1 Pa
      { title: "differential_pressure", res: 0, unit: 8 }, //31 1 hPa
      { title: "temperature", res: 1, unit: 0 }, //32 0.1 °C
      { title: "pyranometer", res: 2, unit: 29 }, //34 0.01 mV
      { title: "uva_irradiance", res: 0, unit: 44 }, //34 1 mW/m2
      { title: "uva_proportion", res: 0, unit: 47 }, //35 1 mW/lumen
      { title: "natural_wet_bulb", res: 1, unit: 0 }, //36 0.1 °C
      { title: "globe_temperature", res: 1, unit: 0 }, //37 0.1 °C
      { title: "wbgt_indoor", res: 1, unit: 0 }, //38 0.1 °C
      { title: "wbgt_outdoor", res: 1, unit: 0 }, //39 0.1 °C
      { title: "illuminance", res: -1, unit: 35 }, //40 10 lux
      { title: "wind_gust", res: 1, unit: 17 }, //41 0.1 m/s
      { title: "differential_pressure", res: 2, unit: 7 }, //42 0.01 Pa
      { title: "max_rain_rate", res: 0, unit: 43 }, //43 1 CNT/h
      { title: "daily_rain", res: 0, unit: 40 }, //44 1 CNT
      { title: "battery_voltage", res: 2, unit: 28 }, //45 0.01 V
      { title: "wind_speed", res: 2, unit: 17 }, //46 0.01 m/s
      { title: "wind_direction", res: 1, unit: 34 }, //47 0.1 DEG
      { title: "mkt", res: 1, unit: 0 }, //48 0.1 °C
      { title: "mkt", res: 1, unit: 0 }, //49 0.1 °C
      { title: "mkt", res: 1, unit: 0 }, //50 0.1 °C
      { title: "contact_input", res: 0, unit: 255 }, //51 1 not def
      { title: "flow", res: 0, unit: 51 }, //52 1 l/s
      { title: "flow", res: 0, unit: 52 }, //53 1 l/min
      { title: "flow", res: 0, unit: 54 }, //54 1 m3/min
      { title: "volumetric_water_content", res: 1, unit: 2 }, //55 0.1 %
      { title: "soil_moisture", res: 1, unit: 29 }, //56 0.1 mV
      { title: "volumetric_water_content", res: 1, unit: 2 }, //57 0.1 %
      { title: "soil_moisture", res: 1, unit: 29 }, //58 0.1 mV
      { title: "air_speed", res: 2, unit: 17 }, //59 0.01 m/s
      { title: "par", res: 0, unit: 56 }, //60 1 umol/(m2s)
      { title: "max_rain_last_hour", res: 0, unit: 40 }, //61 1 CNT
      { title: "gps_direction", res: 1, unit: 34 }, //62 0.1 DEG
      { title: "natural_wet_bulb_computed", res: 1, unit: 0 }, //63 0.1 °C
      { title: "voltage_power_supply", res: 2, unit: 28 }, //64 0.01 V
      { title: "current_rain", res: 0, unit: 40 }, //65 1 CNT
      { title: "sun_presence", res: 0, unit: 255 }, //66 1 not def
      { title: "sun_last_minute", res: 0, unit: 46 }, //67 1 sec
      { title: "sun_last_10_min", res: 0, unit: 40 }, //68 1 CNT
      { title: "acceleration_x", res: 3, unit: 37 }, //69 0.001 g
      { title: "acceleration_y", res: 3, unit: 37 }, //70 0.001 g
      { title: "evapotranspiration_hour", res: 2, unit: 41 }, //71 0.01 mm/h
      { title: "daily_evapotranspiration", res: 2, unit: 57 }, //72 0.01 mm/day
      { title: "net_radiation", res: 0, unit: 22 }, //73 1 W/m2
      { title: "relative_pressure", res: 0, unit: 8 }, //74 1 hPa
      { title: "fluid_level", res: 2, unit: 45 }, //75 0.01 m
      { title: "leaf_wetness_down", res: 1, unit: 33 }, //76 0.1 %
      { title: "leaf_wetness_up", res: 1, unit: 33 }, //77 0.1 %
      { title: "par", res: 1, unit: 56 }, //78 0.1 umol/(m2s)
      { title: "wind_gust", res: 2, unit: 17 }, //79 0.01 m/s
      { title: "wind_gust_direction", res: 1, unit: 34 }, //80 0.1 DEG
      { title: "uva_irradiance", res: 2, unit: 22 }, //81 0.01 W/m2
      { title: "uvb_irradiance", res: 2, unit: 22 }, //82 0.01 W/m2
      { title: "uvc_irradiance", res: 2, unit: 22 }, //83 0.01 W/m2
      { title: "relative_humidity", res: 2, unit: 2 }, //84 0.01 %
      { title: "max_rain_rate", res: 1, unit: 41 }, //85 0.1 mm/h
      { title: "albedo", res: 1, unit: 33 }, //86 0.1 %
      { title: "temperature", res: 2, unit: 0 }, //87 0.01 °C
      { title: "pm1_0", res: 1, unit: 65 }, //88 0.1 ug/m3
      { title: "pm2_5", res: 1, unit: 65 }, //89 0.1 ug/m3
      { title: "pm4_0", res: 1, unit: 65 }, //90 0.1 ug/m3
      { title: "pm10", res: 1, unit: 65 }, //91 0.1 ug/m3
      { title: "typical_particle_size", res: 2, unit: 66 }, //92 0.01 um
  ];
  measSetVect[1] = [
      { title: "temperature", res: 1, unit: 0 }, //128 PT100 2 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //129 PT100 3 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //130 PT100 4 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //131 PT1000 2 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //132 PT1000 3 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //133 PT1000 4 wires 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //135 TC K 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //135 TC J 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //136 TC T 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //137 TC N 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //138 TC R 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //139 TC S 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //140 TC B 0.1 °C
      { title: "temperature", res: 1, unit: 0 }, //141 TC E 0.1 °C
      { title: "voltage", res: 1, unit: 29 }, //142 0-1V 0.1 mV
      { title: "voltage", res: 2, unit: 29 }, //143 0-50 mV 0.01 mV
      { title: "current", res: 2, unit: 30 }, //144 4-20mA 0.01 mA
      { title: "potentiometer", res: 0, unit: 33 }, //145 1 %
      { title: "voltage", res: 0, unit: 255 }, //146 0-1V mapped 1 not def
      { title: "voltage", res: 0, unit: 255 }, //147 0-50mV mapped 1 not def
      { title: "current", res: 0, unit: 255 }, //148 4-20mA mapped 1 not def
      { title: "potentiometer", res: 0, unit: 255 }, //149 mapped 1 not def
      { title: "voltage", res: 0, unit: 29 }, //150 0-10V 1 mV
      { title: "voltage", res: 0, unit: 255 }, //151 0-10V mapped 1 not def
      { title: "digital_measure", res: 0, unit: 255 }, //152 1 not def
      { title: "voltage", res: 2, unit: 29 }, //153 -50...+50mV 0.01 mV
      { title: "voltage", res: 0, unit: 255 }, //154 -50...+50mV mapped 1 not def
      { title: "pyrgeometer", res: 0, unit: 22 }, //155 1 W/m2
      { title: "temperature", res: 1, unit: 0 }, //156 0.1 °C
      { title: "current", res: 3, unit: 30 }, //157 0.001 mA
      { title: "temperature", res: 2, unit: 0 }, //158 PT100 0p01 3 WIRE 0.01 °C
      { title: "temperature", res: 2, unit: 0 }, //159 PT100 0p01 4 WIRE 0.01 °C
      { title: "temperature", res: 2, unit: 0 }, //160 PT1000 0p01 3 WIRE 0.01 °C
      { title: "temperature", res: 2, unit: 0 }, //161 PT1000 0p01 4 WIRE 0.01 °C
      { title: "flow_rate", res: 0, unit: 55 }, //162 1 m3/h
      { title: "digital_measure", res: 0, unit: 255 }, //163 1 not def
  ];
  measSetVect[2] = [
      { title: "counter", res: 0, unit: 40 }, //192 1 CNT
      { title: "counter", res: 0, unit: 40 }, //193 1 CNT
      { title: "mapped_counter", res: 0, unit: 255 }, //194 1 not def
      { title: "mapped_counter", res: 0, unit: 255 }, //195 1 not def
      { title: "total_rain", res: 3, unit: 38 }, //196 0.001 mm
      { title: "total_rain", res: 3, unit: 38 }, //197 0.001 mm
      { title: "daily_rain", res: 3, unit: 38 }, //198 0.001 mm
      { title: "daily_rain", res: 3, unit: 38 }, //199 0.001 mm
      { title: "digital_measure", res: 0, unit: 255 }, //200 1 not def
      { title: "digital_measure", res: 0, unit: 255 }, //201 1 not def
      { title: "total_energy", res: 2, unit: 50 }, //202 0.01 kWh
      { title: "total_energy", res: 2, unit: 50 }, //203 0.01 kWh
      { title: "flow_rate", res: 2, unit: 55 }, //204 0.01 m3/h
      { title: "flow_rate", res: 2, unit: 55 }, //205 0.01 m3/h
      { title: "energy", res: 3, unit: 50 }, //206 0.001 kWh
      { title: "energy", res: 3, unit: 50 }, //207 0.001 kWh
      { title: "energy", res: 3, unit: 67 }, //208 0.001 MWh
      { title: "energy", res: 3, unit: 67 }, //209 0.001 MWh
  ];
  measSetVect[3] = [
      { title: "total_rain", res: 0, unit: 40 }, //252 1 CNT
      { title: "total_rain", res: 0, unit: 40 }, //253 1 CNT
  ];
  var notDefMeas = { title: "not_defined", res: 0, unit: 255 }; //255 1 not def
  var mSetStartIdxVect = [0, 128, 192, 252];
  var mSetLengthVect = [
      measSetVect[0].length,
      measSetVect[1].length,
      measSetVect[2].length,
      measSetVect[3].length,
  ];
  var lppMeasSet = [
      { title: "digital_in", res: 0, unit: 255 }, //0 -> 0
      { title: "digital_out", res: 0, unit: 255 }, //1 -> 1
      { title: "analog_in", res: 2, unit: 255 }, //2 -> 2
      { title: "analog_out", res: 2, unit: 255 }, //3 -> 3
      { title: "illuminance", res: 0, unit: 35 }, //101 -> 4
      { title: "presence", res: 0, unit: 255 }, //102 -> 5
      { title: "temperature", res: 1, unit: 0 }, //103 -> 6
      { title: "relative_humidity", res: 1, unit: 2 }, //104 -> 7
      { title: "acceleration_x", res: 3, unit: 37 }, //113 -> 8
      { title: "acceleration_y", res: 3, unit: 37 }, //113 -> 9
      { title: "acceleration_z", res: 3, unit: 37 }, //113 -> 10
      { title: "atmospheric_pressure", res: 1, unit: 8 }, //115 -> 11
  ];
  
  
  function getMeasureDfltParams(idx) {
      var i = 0;
      var mElem = {};
      for (; i < measSetVect.length; i++){
          if(
              idx >= mSetStartIdxVect[i] &&
              idx < mSetStartIdxVect[i] + mSetLengthVect[i]
          ){
              //NOME MISURA da measSetVect
              mElem = measSetVect[i][idx - mSetStartIdxVect[i]];
              break;
          }
      }
      if (i >= measSetVect.length) mElem = notDefMeas;
      return mElem;
  }
  function vect2Num(bytes, numBytes) {
      var result = 0;
      for (var i = 0; i < numBytes; i++){
          result += bytes[i] << (8 * i);
      }
      return result;
  }
  function hex2SignedIntNum(m) {
      if ((m & 0x8000) > 0){
          m = m - 0x10000;
      }
      return m;
  }
  function hex2SignedInt(bytes) {
      return hex2SignedIntNum(vect2Num(bytes, 2));
  }
  function hex2SignedChar(a) {
      if ((a & 0x80) > 0){
          a = a - 0x100;
      }
      return a;
  }
  function hex2SignedLongNum(a) {
      if ((a & 0x80000000) > 0){
          a = a - 0x100000000;
      }
      return a;
  }
  function hex2SignedLong(bytes) {
      return hex2SignedLongNum(vect2Num(bytes, 4));
  }
  function isConfigurableMeasure(type) {
      switch (type) {
          case 14: //FREQUENCY_USER_CONF_MEAS
          case 146: //VOLTAGE_1V_USER_CONF_MEAS
          case 147: //VOLTAGE_50mV_USER_CONF_MEAS
          case 148: //CURRENT_4_20mA_USER_CONF_MEAS
          case 149: //POTENTIOMETER_USER_CONF_MEAS
          case 151: //VOLTAGE_10V_USER_CONF_MEAS
          case 152: //DIGITAL_SIGNED_INPUT_MEAS
          case 154: //VOLTAGE_m50_p50mV_USER_CONF_MEAS
          case 163: //DIGITAL_SIGNED_INPUT_FLOAT_TO_INT_MEAS
          case 194: //COUNTER_LS_USER_CONF_MEAS
          case 195: //COUNTER_MS_USER_CONF_MEAS
          case 200: //DIGITAL_SIGNED_INPUT_LONG_LS_MEAS
          case 201: //DIGITAL_SIGNED_INPUT_LONG_LS_MEAS
              return 1;
          default:
              return 0;
      }
  }
  function round(value, decimals) {
      return Number(Math.round(value + "e" + decimals) + "e-" + decimals);
  }
  function isLongMeasure(type) {
      return type >= 192 && type != 255 ? 1 : 0;
  }
  function MeasureStruct(type, valueInt, res, unit, alarm, ch) {
      var measDfltParams = getMeasureDfltParams(type);
      this.type = type;
      this.title = measDfltParams.title;
      if (isConfigurableMeasure(type)) {
          this.res = res;
          this.unit = unit;
      } else {
          this.res = measDfltParams.res;
          this.unit = measDfltParams.unit;
      }
      this.alarm = alarm;
      this.value = valueInt * Math.pow(10, -this.res);
      this.value = round(this.value, this.res < 0 ? 0 : this.res);
      this.channel = ch;
      this.valid = type == 255 ? -1 : type;
  }
  function ExtractMeasureStatus(bytes, index) {
      var startb = index * 3;
      var stopb = (index + 1) * 3 - 1;
      var startB = startb >> 3;
      var stopB = stopb >> 3;
      var shift = startb % 8;
      var mask =(vect2Num(bytes.slice(startB), stopB - startB + 1) >> shift) & 0x07;
  
      return mask;
  }
  function mapMeasStatusToFlags(mStatus) {
      switch (mStatus) {
          case 2:
              return 0x01; //low alarm
          case 3:
              return 0x02; //high alarm
          case 4:
              return 0x05; //underflow + low alarm
          case 5:
              return 0x09; //not init + low alarm
          case 6:
              return 0x12; //overflow + high alarm
          case 7:
              return 0x22; //error + high alarm
          default:
              return 0;
      }
  }
  function lppIdx(type, pos) {
      switch (type) {
          case 0:
              return 0;
          case 1:
              return 1;
          case 2:
              return 2;
          case 3:
              return 3;
          case 101:
              return 4;
          case 102:
              return 5;
          case 103:
              return 6;
          case 104:
              return 7;
          case 113:
              return 8 + pos;
          case 115:
              return 11;
          default:
              return -1;
      }
  }
  
  function vect2NumMSB(bytes, n) {
      var result = 0;
      for (var i = 0; i < n; i++){
          result += bytes[i] << (8 * (n - i - 1));
      }
      return result;
  }
  
  function hex2SignedIntMSB(bytes) {
      return hex2SignedIntNum(vect2NumMSB(bytes, 2));
  }
  
  function MeasureStructLPP(type, valueInt, pos, ch) {
      var el = {};
      this.valid = lppIdx(type, pos);
      if (this.valid >= 0) {
          el = lppMeasSet[this.valid];
          this.title = el.title;
          this.res = el.res;
          this.unit = el.unit;
          this.value = valueInt * Math.pow(10, -this.res);
          this.value = round(this.value, this.res < 0 ? 0 : this.res);
          this.channel = ch;
      }
  }
  
  function Decoder(bytes, port) {
      var type, measure, vect, al, i, measStat, pos, end, prop;
      var decoded = {};
      var measureList = [];
  
      console.log("bytes:" + bytes);
  
      if(port == 2 || port == 3){
          prop = 1;
          if (bytes.length < 5) return decoded;
          //decode header
          //batteryLevel = (bytes[4] >> 4) & 0x0007;
          //error = (bytes[4] >> 7) & 0x01;
      }else{
          prop = 0;
      }
      switch (port) {
          case 1: //Cayenne LPP
              pos = 0;
              end = 0;
              while (pos < bytes.length && !end) {
                  vect = bytes.slice(pos);
                  if (vect.length < 3) {
                      end = 1;
                      break;
                  }
                  i = bytes[pos++];
                  type = bytes[pos++];
                  switch (type) {
                      case 0:
                      case 1:
                      case 102:
                          measureList.push(new MeasureStructLPP(type, bytes[pos++], 0, i));
                          break;
                      case 104:
                          measureList.push(new MeasureStructLPP(type, bytes[pos] * 5, 0, i));
                          pos++;
                          break;
                      case 2:
                      case 3:
                      case 103:
                          if (vect.length < 4) {
                              end = 1;
                              break;
                          }
                          measureList.push(
                          new MeasureStructLPP(type, hex2SignedIntMSB(bytes.slice(pos)), 0, i));
                          pos += 2;
                          break;
                      case 101:
                      case 115:
                          if (vect.length < 4) {
                              end = 1;
                              break;
                          }
                          measureList.push(new MeasureStructLPP(type, vect2NumMSB(bytes.slice(pos), 2), 0, i));
                          pos += 2;
                          break;
                      case 113:
                          if (vect.length < 8) {
                              end = 1;
                              break;
                          }
                          for (var s = 0; s < 3; s++){
                              measureList.push(new MeasureStructLPP(type, hex2SignedIntMSB(bytes.slice(pos + s * 2)), s, i));
                          }
                          pos += 6;
                          break;
                      case 134:
                          pos += 6;
                          break;
                      case 136:
                          pos += 9;
                          break;
                      default:
                          end = 1;
                          break;
                  }
              }
              break;
          case 2:
              pos = 5;
              for (i = 0; i < 12 && pos < bytes.length; i++) {
                  measStat = ExtractMeasureStatus(bytes, i);
                  if (measStat > 0) {
                      vect = bytes.slice(pos);
                      if (vect.length < 1){
                          break;
                      }
                      type = bytes[pos++];
                      al = mapMeasStatusToFlags(measStat);
                      if (type >= 192 && type < 254){
                          if (vect.length < 5){
                              break;
                          }
                          measure = hex2SignedLong(bytes.slice(pos)); //prima LS e poi MS
                          pos += 4;
                      }else{
                          if (vect.length < 3){
                              break;
                          }
                          measure = hex2SignedInt(bytes.slice(pos));
                          pos += 2;
                      }
                      measureList.push(new MeasureStruct(type, measure, 0, 255, al, i + 1));
                  }
              }
              break;
          case 3:
              pos = 5;
              for (i = 0; i < 12 && pos < bytes.length; i++) {
                  measStat = ExtractMeasureStatus(bytes, i);
                  if(measStat > 0){
                      vect = bytes.slice(pos);
                      if(vect.length < 3){
                          break;
                      }
                      type = bytes[pos++];
                      al = mapMeasStatusToFlags(measStat);
                      if(type >= 192 && type < 254){
                          if(vect.length < 7){
                              break;
                          }
                          measure = hex2SignedLong(bytes.slice(pos)); //prima LS e poi MS
                          pos += 4;
                      }else{
                          if (vect.length < 5){
                              break;
                          }
                          measure = hex2SignedInt(bytes.slice(pos));
                          pos += 2;
                      }
                      measureList.push(new MeasureStruct(type, measure, hex2SignedChar(bytes[pos + 1]), bytes[pos], al, i + 1));
                      pos += 2;
                  }
              }
              break;
      }
  
      const dataArr = [];         // 送信データ
      for (i = 0; i < measureList.length; i++) {
          const sensorArr =[];
          sensorArr.push({
              name: measureList[i].title,
              value: measureList[i].value,
          });
          dataArr.push({
              channel: measureList[i].channel,
              data: sensorArr,
          });
  
      }
      //debug_print(JSON.stringify(dataArr));
      
      return dataArr;
  }
  
  var unitVect = [
      "°C",
      "°F",
      "%",
      "g/m^3",
      "g/kg",
      "mbar",
      "bar",
      "Pa",
      "hPa",
      "kPa",
      "atm",
      "mmHg",
      "mmH2O",
      "inchHg",
      "inchH2O",
      "kgf/cm^2",
      "PSI",
      "m/s",
      "km/h",
      "ft/sec",
      "mph",
      "knot",
      "W/m^2",
      "uW/cm^2",
      "Wh/m^2",
      "kWh/m^2",
      "J/m^2",
      "uJ/cm^2",
      "V",
      "mV",
      "mA",
      "ppm",
      "Hz",
      "%",
      "DEG",
      "lux",
      "m/s^2",
      "g",
      "mm",
      "inch",
      "CNT",
      "mm/h",
      "inch/h",
      "CNT/h",
      "mW/m^2",
      "m",
      "s",
      "uW/lm",
      "dB",
      "dB(A)",
      "kWh",
      "l/s",
      "l/min",
      "gal/min",
      "m^3/min",
      "m^3/h",
      "umol/(m^2s)",
      "mm/d",
      "kV",
      "A",
      "kA",
      "cm/s",
      "klux",
      "m^3",
      "g/(m^2s)",
      "ug/m^3",
      "um",
      "MWh",
      "pH",
  ];
  
  function hex2dec(str, numBytes) {
      //debug_print("hex2dec str:"+str + " numBytes:" + numBytes);
      var result = 0;
      for (var i = 0; i < numBytes; i++){
          result += parseInt(str.slice(i*2, i*2+2), 16) << (8 * i);
      }
      return result;
  }