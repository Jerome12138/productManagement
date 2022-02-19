import axios from '@/libs/api.request'

export const getScenario = productType => {
  return axios.request({
    url: 'scenario/getScenarioByType?productType=' + productType,
    method: 'post'
  })
}
export const queryProduct = condition => {
  return axios.request({
    url: 'product/queryProduct',
    data: condition,
    method: 'post'
  })
}
export const getFunctionByType = productType => {
  return axios.request({
    url: 'function/getFunctionByType',
    method: 'post'
  })
}
export const getScenarioByType = productType => {
  return axios.request({
    url: 'scenario/getScenarioByType?productType=' + productType,
    method: 'post'
  })
}
export const deleteFunctionById = id => {
  return axios.request({
    url: 'function/deleteFunctionById?id=' + id,
    method: 'post'
  })
}
export const deleteScenarioById = id => {
  return axios.request({
    url: 'scenario/deleteScenarioById?id=' + id,
    method: 'post'
  })
}
export const deleteProductById = id => {
  return axios.request({
    url: 'product/deleteProductById?id=' + id,
    method: 'post'
  })
}
export const deleteSelectedProductByIds = params => {
  return axios.request({
    url: 'product/deleteBatchProductByIds',
    data: params,
    method: 'post'
  })
}

export const saveScenario = params => {
  return axios.request({
    url: 'scenario/saveScenario',
    data: params,
    method: 'post'
  })
}
export const updateScenario = params => {
  return axios.request({
    url: 'scenario/saveScenario',
    data: params,
    method: 'post'
  })
}
export const saveFunction = params => {
  return axios.request({
    url: 'function/saveFunction',
    data: params,
    method: 'post'
  })
}

export const updateFunction = params => {
  return axios.request({
    url: 'function/saveFunction',
    data: params,
    method: 'post'
  })
}
export const getProductCategoryByProductType = productType => {
  return axios.request({
    url: 'dict/getProductCategoryByType?productType=' + productType,
    method: 'post'
  })
}
export const getBranchList = () => {
  return axios.request({
    url: 'dict/getProductBranch',
    method: 'post'
  })
}
export const saveBranch = params => {
  return axios.request({
    url: 'dict/saveBranch',
    data: params,
    method: 'post'
  })
}
export const deleteBranchByCode = code => {
  return axios.request({
    url: 'dict/deleteBranchByCode?code=' + code,
    method: 'post'
  })
}
export const getProductType = () => {
  return axios.request({
    url: 'dict/getProductType',
    method: 'post'
  })
}
export const getProductTypeByTypeCode = productType => {
  return axios.request({
    url: 'dict/getProductTypeByTypeCode?productType=' + productType,
    method: 'post'
  })
}
export const saveProduct = params => {
  return axios.request({
    url: 'product/saveProduct',
    data: params,
    method: 'post'
  })
}
export const getAllUser = () => {
  return axios.request({
    url: 'user/getAllUser',
    method: 'post'
  })
}
export const getAllUserIdAndName = () => {
  return axios.request({
    url: 'user/getAllUserIdAndName',
    method: 'post'
  })
}
export const getAllAuth = () => {
  return axios.request({
    url: 'user/getAllAuth',
    method: 'post'
  })
}
export const saveUser = userData => {
  return axios.request({
    url: 'user/saveUser',
    data: userData,
    method: 'post'
  })
}
export const deleteUserById = userId => {
  return axios.request({
    url: 'user/deleteUserById?userId=' + userId,
    method: 'post'
  })
}

export const getVoiceFunction = () => {
  return axios.request({
    url: 'voiceFunction/getVoiceFunction',
    method: 'post'
  })
}
export const deleteVoiceFunctionById = id => {
  return axios.request({
    url: 'voiceFunction/deleteVoiceFunctionById?id=' + id,
    method: 'post'
  })
}
export const saveVoiceFunction = voiceFunction => {
  return axios.request({
    url: 'voiceFunction/saveVoiceFunction',
    data: voiceFunction,
    method: 'post'
  })
}

export const getEcologyEntrance = () => {
  return axios.request({
    url: 'ecologyEntrance/getEcologyEntrance',
    method: 'post'
  })
}
export const saveEcologyEntrance = ecologyEntrance => {
  return axios.request({
    url: 'ecologyEntrance/saveEcologyEntrance',
    data: ecologyEntrance,
    method: 'post'
  })
}
export const deleteEcologyEntranceById = id => {
  return axios.request({
    url: 'ecologyEntrance/deleteEcologyEntranceById?id=' + id,
    method: 'post'
  })
}
export const saveSensor = params => {
  return axios.request({
    url: 'sensor/saveSensor',
    data: params,
    method: 'post'
  })
}
export const deleteSensorById = id => {
  return axios.request({
    url: 'sensor/deleteSensorById?id=' + id,
    method: 'post'
  })
}
export const getSensorByType = productType => {
  return axios.request({
    url: 'sensor/getSensorByType?productType=' + productType,
    method: 'post'
  })
}
export const queryAuditGroupByUserId = id => {
  return axios.request({
    url: 'auditGroup/queryAuditGroupByUserId?id=' + id,
    method: 'post'
  })
}
export const saveAuditGroup = auditGroup => {
  return axios.request({
    url: 'auditGroup/saveAuditGroup',
    data: auditGroup,
    method: 'post'
  })
}
export const deleteAuditGroupById = id => {
  return axios.request({
    url: 'auditGroup/deleteAuditGroupById?id=' + id,
    method: 'post'
  })
}
export const saveTask = params => {
  return axios.request({
    url: 'task/saveTask',
    data: params,
    method: 'post'
  })
}
export const queryUnhandledTaskList = userId => {
  return axios.request({
    url: 'task/queryUnhandledTaskList?userId=' + userId,
    method: 'post'
  })
}
export const queryHandledTaskList = userId => {
  return axios.request({
    url: 'task/queryHandledTaskList?userId=' + userId,
    method: 'post'
  })
}
export const getTaskDetailById = taskId => {
  return axios.request({
    url: 'task/getTaskDetailById?taskId=' + taskId,
    method: 'post'
  })
}
export const handleTaskProcess = params => {
  return axios.request({
    url: 'task/handleTaskProcess',
    data: params,
    method: 'post'
  })
}
export const getProductModel = () => {
  return axios.request({
    url: 'product/getProductModel',
    method: 'post'
  })
}
export const getTableData = () => {
  return axios.request({
    url: 'get_table_data',
    method: 'get'
  })
}

export const getDragList = () => {
  return axios.request({
    url: 'get_drag_list',
    method: 'get'
  })
}

export const errorReq = () => {
  return axios.request({
    url: 'error_url',
    method: 'post'
  })
}

export const saveErrorLogger = info => {
  return axios.request({
    url: 'save_error_logger',
    data: info,
    method: 'post'
  })
}

export const uploadImg = formData => {
  return axios.request({
    url: 'image/upload',
    data: formData
  })
}

export const getOrgData = () => {
  return axios.request({
    url: 'get_org_data',
    method: 'get'
  })
}

export const getTreeSelectData = () => {
  return axios.request({
    url: 'get_tree_select_data',
    method: 'get'
  })
}

export const getFunctionType = productType => {
  return axios.request({
    url: 'function/getFunctionType',
    method: 'post'
  })
}

export const getHeatingTubeType = () => {
  return axios.request({
    url: 'function/getHeatingTubeType',
    method: 'post'
  })
}

export const getWifiModuleType = () => {
  return axios.request({
    url: 'function/getWifiModuleType',
    method: 'post'
  })
}

export const getElectricBoardInfo = productType => {
  return axios.request({
    url: 'electricBoardInfo/getElectricBoardInfo?productType=' + productType,
    method: 'post'
  })
}

export const getSelectOption = productType => {
  return axios.request({
    url: `selectOption/getSelectOption?productType=${productType}`,
    method: 'post'
  })
}
