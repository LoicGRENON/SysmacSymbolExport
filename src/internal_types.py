
sAXIS_REF_STA = """
<DataType Name="_sAXIS_REF_STA" BaseType="STRUCT" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="14" OffsetType="NJ">
  <DataType Name="Ready" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Disabled" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Standstill" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Discrete" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Continuous" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Synchronized" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Homing" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Stopping" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="ErrorStop" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Coordinated" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Reserved" BaseType="ARRAY[0..7] OF BYTE" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
</DataType>
"""

sAXIS_REF_DET = """
<DataType Name="_sAXIS_REF_STA" BaseType="STRUCT" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="14" OffsetType="NJ">
  <DataType Name="Idle" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="InPosWaiting" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Homed" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="InHome" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="VelLimit" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Reserved" BaseType="ARRAY[0..7] OF BYTE" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
</DataType>
"""

sAXIS_REF_STA_DRV = """
<DataType Name="_sAXIS_REF_STA" BaseType="STRUCT" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="14" OffsetType="NJ">
  <DataType Name="ServoOn" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Ready" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="MainPower" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="P_OT" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="N_OT" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="HomeSw" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Home" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="ImdStop" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Latch1" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Latch2" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="DrvAlarm" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="DrvWarning" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="ILA" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="CSP" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="CSV" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="CST" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Reserved" BaseType="ARRAY[0..7] OF BYTE" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
</DataType>
"""

sMC_REF_EVENT = """
<DataType Name="_sAXIS_REF_STA" BaseType="STRUCT" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="14" OffsetType="NJ">
  <DataType Name="Active" BaseType="BOOL" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
  <DataType Name="Code" BaseType="WORD" ArrayType="" Length="" InitialValue="" EnumValue="" Comment="" OffsetChannel="" OffsetBit="" IsControllerDefinedType="false" Order="0" OffsetType="" />
</DataType>
"""