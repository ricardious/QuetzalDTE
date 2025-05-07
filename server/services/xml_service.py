import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from models.dte import DTE
from config import Config


class XMLService:
    def __init__(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        self.path = Config.AUTHORIZATIONS_FILE
        if not os.path.exists(self.path):
            self._init_file()

    def _init_file(self):
        root = ET.Element("LISTAAUTORIZACIONES")  # Cambiado a nombre en español
        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(reparsed.toprettyxml(indent="  "))
            
    def read_requests(self, xml_file) -> list[DTE]:
        requests = []
        try:
            tree = ET.parse(xml_file)
            for elem in tree.getroot().findall(".//DTE"):
                try:
                    dto = DTE(
                        timestamp=elem.findtext("TIEMPO"),
                        reference=elem.findtext("REFERENCIA"),
                        issuer_nit=elem.findtext("NIT_EMISOR"),
                        receiver_nit=elem.findtext("NIT_RECEPTOR"),
                        amount=float(elem.findtext("VALOR") or 0),
                        vat=float(elem.findtext("IVA") or 0),
                        total=float(elem.findtext("TOTAL") or 0),
                    )
                    requests.append(dto)
                except Exception:
                    continue
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        return requests

    def save_authorizations(self, result):
        if os.path.exists(self.path):
            tree = ET.parse(self.path)
            root = tree.getroot()
        else:
            root = ET.Element("LISTAAUTORIZACIONES") 
            
        for summary in result["summaries"]:
            auth_el = ET.SubElement(root, "AUTORIZACION")
            ET.SubElement(auth_el, "FECHA").text = summary["date"]
            ET.SubElement(auth_el, "FACTURAS_RECIBIDAS").text = str(summary["received"])
            
            errs_el = ET.SubElement(auth_el, "ERRORES")
            error_mapping = {
                "issuer_nit": "NIT_EMISOR",
                "receiver_nit": "NIT_RECEPTOR", 
                "vat": "IVA",
                "total": "TOTAL",
                "duplicate_reference": "REFERENCIA_DUPLICADA"
            }
            for k, v in summary["errors"].items():
                ET.SubElement(errs_el, error_mapping[k]).text = str(v)
            
            ET.SubElement(auth_el, "FACTURAS_CORRECTAS").text = str(summary["correct"])
            ET.SubElement(auth_el, "CANTIDAD_EMISORES").text = str(summary["unique_issuers"])
            ET.SubElement(auth_el, "CANTIDAD_RECEPTORES").text = str(summary["unique_receivers"])

            auth_list_el = ET.SubElement(auth_el, "LISTADO_AUTORIZACIONES")
            if "approvals" in summary:
                for doc in summary["approvals"]:
                    aprobacion_el = ET.SubElement(auth_list_el, "APROBACION")
                    
                    nit_emisor_el = ET.SubElement(aprobacion_el, "NIT_EMISOR")
                    nit_emisor_el.text = doc["issuer_nit"]
                    nit_emisor_el.set("ref", doc["reference"])  # Agregar atributo ref
                    
                    ET.SubElement(aprobacion_el, "CODIGO_APROBACION").text = doc["approval_code"]
                
                ET.SubElement(auth_list_el, "TOTAL_APROBACIONES").text = str(len(summary["approvals"]))
            rough_string = ET.tostring(root, encoding="utf-8")
            reparsed = minidom.parseString(rough_string)
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

    def read_authorizations(self):
        tree = ET.parse(self.path)
        out = []
        for elem in tree.getroot().findall("AUTORIZACION"):
            auth_data = {}
            error_mapping = {
                "NIT_EMISOR": "issuer_nit",
                "NIT_RECEPTOR": "receiver_nit", 
                "IVA": "vat",
                "TOTAL": "total",
                "REFERENCIA_DUPLICADA": "duplicate_reference"
            }
            
            field_mapping = {
                "FECHA": "date",
                "FACTURAS_RECIBIDAS": "received",
                "FACTURAS_CORRECTAS": "correct",
                "CANTIDAD_EMISORES": "unique_issuers", 
                "CANTIDAD_RECEPTORES": "unique_receivers"
            }
            
            for child in elem:
                if child.tag == "ERRORES":
                    errors = {}
                    for error in child:
                        if error.tag in error_mapping:
                            errors[error_mapping[error.tag]] = error.text
                    auth_data["errors"] = errors
                elif child.tag == "LISTADO_AUTORIZACIONES":
                    auth_list = []
                    for doc_elem in child.findall("APROBACION"):
                        doc_data = {}
                        
                        nit_emisor = doc_elem.find("NIT_EMISOR")
                        if nit_emisor is not None:
                            doc_data["issuer_nit"] = nit_emisor.text
                            if "ref" in nit_emisor.attrib:
                                doc_data["reference"] = nit_emisor.attrib["ref"]
                        
                        codigo = doc_elem.find("CODIGO_APROBACION")
                        if codigo is not None:
                            doc_data["approval_code"] = codigo.text
                        
                        auth_list.append(doc_data)
                    auth_data["approvals"] = auth_list
                elif child.tag in field_mapping:
                    auth_data[field_mapping[child.tag]] = child.text
            
            out.append(auth_data)
        return {"authorizations": out}

    def reset_authorizations(self):
        self._init_file()
